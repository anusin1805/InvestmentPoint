import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import time
import requests_cache

# --- 1. INITIALIZE CACHING ---
try:
    session = requests_cache.CachedSession('yfinance.cache')
    session.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
except Exception:
    session = None

st.set_page_config(page_title="US Market Dashboard - Live Data", layout="wide")

# --- 2. DATA ENGINE ---
@st.cache_data(ttl=3600)
def get_cached_data(symbol, period, interval):
    try:
        ticker = yf.Ticker(symbol, session=session)
        time.sleep(0.2) # To avoid rate limiting
        data = ticker.history(period=period, interval=interval)
        return data
    except Exception:
        return None

# --- 3. MASTER DATABASE ---
master_db = {
    "Apple": "AAPL", "Microsoft": "MSFT", "Alphabet (Class A)": "GOOGL",
    "Amazon": "AMZN", "NVIDIA": "NVDA", "Meta Platforms": "META",
    "Tesla": "TSLA", "Broadcom": "AVGO", "Berkshire Hathaway": "BRK.B"
}

# --- 4. SIDEBAR ---
st.sidebar.header("📊 Chart Settings")
timeframe_choice = st.sidebar.radio(
    "Select timeframe:",
    options=["7d (Daily)", "1mo (Daily)", "6mo (Daily)", "1y (Daily)", "5y (Weekly)", "Max (Monthly)"],
    index=1
)

# --- 5. CHARTING FUNCTION ---
def plot_stock_chart(symbol, name, timeframe):
    tm_map = {
        "7d (Daily)": ("7d", "1d"), "1mo (Daily)": ("1mo", "1d"),
        "6mo (Daily)": ("6mo", "1d"), "1y (Daily)": ("1y", "1d"),
        "5y (Weekly)": ("5y", "1wk"), "Max (Monthly)": ("max", "1mo")
    }
    period, interval = tm_map[timeframe]
    data = get_cached_data(symbol, period, interval)

    if data is not None and not data.empty:
        # Calculate Moving Average for trend analysis
        data['MA50'] = data['Close'].rolling(window=50).mean()
        
        # Display Header
        st.subheader(f"{name} ({symbol})")
        
        # Plotting
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(data.index, data['Close'], label="Close Price", color="#1f77b4")
        if len(data) > 50:
            ax.plot(data.index, data['MA50'], label="50-day MA", color="orange", linestyle="--")
        
        ax.set_ylabel("Price ($)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Render the plot in Streamlit
        st.pyplot(fig)

        # DOWNLOAD CSV BUTTON
        csv = data.to_csv().encode('utf-8')
        st.download_button(
            label=f"📥 Download {symbol} CSV",
            data=csv,
            file_name=f"{symbol}_data.csv",
            mime='text/csv',
            key=f"btn_{symbol}" # Must be unique for each stock
        )
        st.divider()
    else:
        st.error(f"⚠️ No data found for {name} ({symbol})")

# --- 6. MAIN DISPLAY & EXECUTION ---
st.title("📈 US Market Dashboard with Trends")

# This creates the dropdown selector
selected_stocks = st.multiselect(
    "Select stocks to view:", 
    options=list(master_db.keys()), 
    default=["Apple", "Microsoft"]
)

# THIS IS THE CRITICAL LOOP THAT SHOWS THE CHARTS
if selected_stocks:
    for name in selected_stocks:
        symbol = master_db[name]
        # We call the function here to actually draw the chart
        plot_stock_chart(symbol, name, timeframe_choice)
else:
    st.info("Please select at least one stock from the dropdown above to view charts.")
