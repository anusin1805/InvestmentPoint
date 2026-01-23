import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import time

# --- 1. CONFIG ---
st.set_page_config(page_title="US Market Dashboard", layout="wide")

# --- 2. THE DATA ENGINE (Native Streamlit Caching) ---
@st.cache_data(ttl=3600)
def get_stock_data(symbol, period, interval):
    try:
        ticker = yf.Ticker(symbol)
        # Small delay to prevent being blocked by Yahoo Finance
        time.sleep(0.5) 
        df = ticker.history(period=period, interval=interval)
        return df if not df.empty else None
    except Exception:
        return None

# --- 3. MASTER DATABASE ---
master_db = {
    "Apple": "AAPL", "Microsoft": "MSFT", "Alphabet (Class A)": "GOOGL",
    "Amazon": "AMZN", "NVIDIA": "NVDA", "Meta Platforms": "META",
    "Tesla": "TSLA", "Broadcom": "AVGO", "Berkshire Hathaway": "BRK.B"
}

# --- 4. UI: TITLE & SIDEBAR ---
st.title("📈 US Market Dashboard")

st.sidebar.header("📊 Settings")
timeframe = st.sidebar.radio(
    "Select timeframe:",
    options=["7d", "1mo", "6mo", "1y", "5y", "max"],
    index=1
)

# Mapping intervals to periods
interval_map = {"7d": "1d", "1mo": "1d", "6mo": "1d", "1y": "1d", "5y": "1wk", "max": "1mo"}
current_interval = interval_map[timeframe]

# --- 5. SELECTOR ---
selected_stocks = st.multiselect(
    "Select stocks to view:", 
    options=list(master_db.keys()), 
    default=["Apple", "Microsoft"]
)

# --- 6. EXECUTION LOOP ---
if selected_stocks:
    for name in selected_stocks:
        symbol = master_db[name]
        data = get_stock_data(symbol, timeframe, current_interval)

        if data is not None:
            st.subheader(f"{name} ({symbol})")
            
            # --- CREATE CHART ---
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(data.index, data['Close'], label="Close Price", color="#1f77b4")
            
            # Simple Trendline (Moving Average)
            if len(data) > 20:
                data['MA20'] = data['Close'].rolling(window=20).mean()
                ax.plot(data.index, data['MA20'], label="20-day MA", color="orange", linestyle="--")
            
            ax.set_ylabel("Price ($)")
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # THIS COMMAND DISPLAYS THE CHART
            st.pyplot(fig)

            # --- DOWNLOAD BUTTON ---
            csv = data.to_csv().encode('utf-8')
            st.download_button(
                label=f"📥 Download {symbol} CSV",
                data=csv,
                file_name=f"{symbol}_data.csv",
                mime='text/csv',
                key=f"dl_{symbol}"
            )
            st.divider()
        else:
            st.error(f"Could not fetch data for {name}. The API might be rate-limiting your request.")
else:
    st.info("Select stocks from the menu to see performance charts.")
