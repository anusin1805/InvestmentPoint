import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import time
import requests_cache

# --- 0. INITIALIZE CACHING SESSION ---
# This mimics a browser and caches requests locally
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

st.set_page_config(page_title="US Market Dashboard - Live Data", layout="wide")

# --- 1. DATA CACHING ENGINE ---
@st.cache_data(ttl=3600)  # Data stays fresh for 1 hour
def get_cached_data(symbol, period, interval):
    try:
        ticker = yf.Ticker(symbol, session=session)
        # Add a tiny delay to prevent rapid-fire requests
        time.sleep(0.2) 
        data = ticker.history(period=period, interval=interval)
        return data
    except Exception:
        return None

# --- 2. MASTER DATABASE ---
master_db = {
    "Apple": "AAPL", "Microsoft": "MSFT", "Alphabet (Class A)": "GOOGL",
    "Amazon": "AMZN", "NVIDIA": "NVDA", "Meta Platforms": "META",
    "Tesla": "TSLA", "Broadcom": "AVGO", "Berkshire Hathaway": "BRK.B",
    "Taiwan Semiconductor (ADR)": "TSM", "UnitedHealth": "UNH",
    "Johnson & Johnson": "JNJ", "Visa": "V", "ExxonMobil": "XOM",
    "JPMorgan Chase": "JPM", "Eli Lilly": "LLY", "Procter & Gamble": "PG",
    "Mastercard": "MA", "Walmart": "WMT", "Chevron": "CVX",
    "AbbVie": "ABBV", "Merck": "MRK", "Pfizer": "PFE",
    "Coca-Cola": "KO", "PepsiCo": "PEP"
}

# --- 3. TICKER RIBBON (Optimized) ---
indices = {
    "S&P 500": "^GSPC",
    "Russell 2000": "^RUT",
    "NYSE Composite": "^NYA",
    "Dow Jones Industrial Average": "^DJI"
}
ribbon_cols = st.columns(len(indices))

for i, (name, sym) in enumerate(indices.items()):
    idx_data = get_cached_data(sym, "2d", "1d")
    if idx_data is not None and len(idx_data) >= 2:
        price = idx_data['Close'].iloc[-1]
        prev = idx_data['Close'].iloc[-2]
        change = ((price - prev) / prev) * 100
        ribbon_cols[i].metric(name, f"{price:,.2f}", f"{change:.2f}%")
    else:
        ribbon_cols[i].warning("Limit Reached")

st.divider()

# --- 4. SIDEBAR ---
st.sidebar.header("📊 Chart Settings")
timeframe_choice = st.sidebar.radio(
    "Select timeframe:",
    options=["7d (Daily)", "1mo (Daily)", "6mo (Daily)", "1y (Daily)", "5y (Weekly)", "Max (Monthly)"],
    index=1
)

# --- 5. CHARTING LOGIC ---
def plot_stock_chart(symbol, name, timeframe):
    # Mapping timeframe to Yahoo periods
    tm_map = {
        "7d (Daily)": ("7d", "1d"),
        "1mo (Daily)": ("1mo", "1d"),
        "6mo (Daily)": ("6mo", "1d"),
        "1y (Daily)": ("1y", "1d"),
        "5y (Weekly)": ("5y", "1wk"),
        "Max (Monthly)": ("max", "1mo")
    }
    period, interval = tm_map[timeframe]
    
    data = get_cached_data(symbol, period, interval)

    if data is None or data.empty:
        st.error(f"Could not load {name}")
        return

    # Moving averages
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data.index, data['Close'], label="Price", color="#1f77b4", linewidth=2)
    
    # Only plot MAs if we have enough data points
    if len(data) > 50:
        ax.plot(data.index, data['MA50'], label="50-day MA", color="orange", alpha=0.8)
    if len(data) > 200:
        ax.plot(data.index, data['MA200'], label="200-day MA", color="red", alpha=0.8)
    
    ax.set_title(f"{name} ({symbol})")
    ax.legend(loc="upper left")
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Volume overlay
    ax2 = ax.twinx()
    ax2.fill_between(data.index, 0, data['Volume'], alpha=0.15, color="gray", label="Volume")
    ax2.set_yticks([]) # Hide volume scale for clean look

    st.pyplot(fig)

# --- 6. MAIN DISPLAY ---
st.title("📈 US Market Dashboard with Trends")

# Optimization: Only show 5 stocks at a time or use a selectbox
# Loading 25 charts at once will ALMOST ALWAYS trigger a rate limit on Streamlit Cloud
selected_stocks = st.multiselect("Select stocks to view:", options=list(master_db.keys()), default=list(master_db.keys())[:5])

for name in selected_stocks:
    symbol = master_db[name]
    plot_stock_chart(symbol, name, timeframe_choice)

st.caption("Data is cached for 1 hour to prevent API blocking.")
