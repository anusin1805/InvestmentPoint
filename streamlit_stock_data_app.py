import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(page_title="US Market Dashboard - Live Data", layout="wide")

# --- 1. MASTER DATABASE (25 largest US mega-cap stocks)
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

# --- 2. TICKER RIBBON (Major US indices)
indices = {
    "S&P 500": "^GSPC",
    "Russell 2000": "^RUT",
    "NYSE Composite": "^NYA",
    "Dow Jones Industrial Average": "^DJI"
}
ribbon_cols = st.columns(len(indices))

for i, (name, sym) in enumerate(indices.items()):
    try:
        idx_data = yf.Ticker(sym).history(period="2d")
        if len(idx_data) >= 2:
            price = idx_data['Close'].iloc[-1]
            prev = idx_data['Close'].iloc[-2]
            change = ((price - prev) / prev) * 100
            ribbon_cols[i].metric(name, f"{price:,.2f}", f"{change:.2f}%")
    except Exception:
        ribbon_cols[i].error(name)

st.divider()

# --- 3. Sidebar Controls ---
st.sidebar.header("📊 Chart Settings")
timeframe = st.sidebar.radio(
    "Select timeframe:",
    options=["7d (Daily)", "1mo (Daily)", "6mo (Daily)", "1y (Daily)", "5y (Weekly)", "Max (Monthly)"],
    index=0
)

# --- Helper function for charts ---
def plot_stock_chart(symbol, name, timeframe):
    ticker = yf.Ticker(symbol)

    if "7d" in timeframe:
        data = ticker.history(period="7d", interval="1d")
    elif "1mo" in timeframe:
        data = ticker.history(period="1mo", interval="1d")
    elif "6mo" in timeframe:
        data = ticker.history(period="6mo", interval="1d")
    elif "1y" in timeframe:
        data = ticker.history(period="1y", interval="1d")
    elif "5y" in timeframe:
        data = ticker.history(period="5y", interval="1wk")
    else:
        data = ticker.history(period="max", interval="1mo")

    if data.empty:
        st.warning(f"No data for {name}")
        return

    # Moving averages
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()

    # Plot price + MAs
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data.index, data['Close'], label="Close Price", color="blue")
    ax.plot(data.index, data['MA50'], label="50-day MA", color="orange")
    ax.plot(data.index, data['MA200'], label="200-day MA", color="red")
    ax.set_title(f"{name} – {timeframe}")
    ax.set_ylabel("Price ($)")
    ax.legend()

    # Volume bars
    ax2 = ax.twinx()
    ax2.bar(data.index, data['Volume'], alpha=0.2, color="gray", label="Volume")
    ax2.set_ylabel("Volume")

    st.pyplot(fig)

# --- 4. Main Display ---
st.title("📈 US Market Dashboard with Trends")

watchlist = list(master_db.keys())  # default: all 25 mega-cap stocks

for name in watchlist:
    symbol = master_db[name]
    st.subheader(name)
    plot_stock_chart(symbol, name, timeframe)

st.caption("Note: Data is delayed. Refresh to update prices.")
