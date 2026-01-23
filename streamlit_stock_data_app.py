import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import time
import requests_cache

# --- 1. INITIALIZE CACHING (Must be first) ---
try:
    session = requests_cache.CachedSession('yfinance.cache')
    session.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
except Exception:
    session = None # Fallback if cache fails

st.set_page_config(page_title="US Market Dashboard - Live Data", layout="wide")

# --- 2. DEFINE THE FUNCTION (Must be before calling it) ---
@st.cache_data(ttl=3600)
def get_cached_data(symbol, period, interval):
    try:
        # Pass the session to yfinance to prevent rate limits
        ticker = yf.Ticker(symbol, session=session)
        time.sleep(0.2) # Throttle requests
        data = ticker.history(period=period, interval=interval)
        return data
    except Exception:
        return None

# --- 3. MASTER DATABASE ---
master_db = {
    "Apple": "AAPL", "Microsoft": "MSFT", "Alphabet (Class A)": "GOOGL",
    "Amazon": "AMZN", "NVIDIA": "NVDA", "Meta Platforms": "META",
    "Tesla": "TSLA", "Broadcom": "AVGO", "Berkshire Hathaway": "BRK.B",
    "JPMorgan Chase": "JPM", "Visa": "V", "Eli Lilly": "LLY"
}

# --- 4. TICKER RIBBON (Now it knows what 'get_cached_data' is) ---
indices = {
    "S&P 500": "^GSPC",
    "Russell 2000": "^RUT",
    "NYSE Composite": "^NYA",
    "Dow Jones Industrial Average": "^DJI"
}

st.title("📈 US Market Dashboard with Trends")
ribbon_cols = st.columns(len(indices))

for i, (name, sym) in enumerate(indices.items()):
    idx_data = get_cached_data(sym, "2d", "1d") # This was line 53 causing the error
    if idx_data is not None and len(idx_data) >= 2:
        price = idx_data['Close'].iloc[-1]
        prev = idx_data['Close'].iloc[-2]
        change = ((price - prev) / prev) * 100
        ribbon_cols[i].metric(name, f"{price:,.2f}", f"{change:.2f}%")

st.divider()

# --- 5. SIDEBAR & CHARTING ---
st.sidebar.header("📊 Chart Settings")
timeframe_choice = st.sidebar.radio(
    "Select timeframe:",
    options=["7d (Daily)", "1mo (Daily)", "6mo (Daily)", "1y (Daily)", "5y (Weekly)", "Max (Monthly)"]
)

def plot_stock_chart(symbol, name, timeframe):
    tm_map = {
        "7d (Daily)": ("7d", "1d"), "1mo (Daily)": ("1mo", "1d"),
        "6mo (Daily)": ("6mo", "1d"), "1y (Daily)": ("1y", "1d"),
        "5y (Weekly)": ("5y", "1wk"), "Max (Monthly)": ("max", "1mo")
    }
    period, interval = tm_map[timeframe]
    data = get_cached_data(symbol, period, interval)

    if data is not None and not data.empty:
        # Add Moving Averages
        data['MA50'] = data['Close'].rolling(window=50).mean()
        
        # Create Chart
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(data.index, data['Close'], label="Price")
        if len(data) > 50:
            ax.plot(data.index, data['MA50'], label="50-day MA")
        ax.set_title(f"{name} Trends")
        ax.legend()
        st.pyplot(fig)

        # DOWNLOAD BUTTON
        csv = data.to_csv().encode('utf-8')
        st.download_button(
            label=f"📥 Download {name} Data",
            data=csv,
            file_name=f"{symbol}_data.csv",
            mime='text/csv',
            key=f"dl_{symbol}" # Unique key for each button
        )

# --- 6. DISPLAY SELECTOR ---
selected_stocks = st.multiselect("Select stocks:", options=list(master_db.keys()), default=list(master_db.keys())[:3])

for name in selected_stocks:
    plot_stock_chart(master_db[name], name, timeframe_choice)
