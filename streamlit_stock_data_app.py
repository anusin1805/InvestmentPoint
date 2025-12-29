import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Investment Point - Live Data", layout="wide")

st.title("📈 Investment Point: Live Market Dashboard")
st.write("Fetching live data from Yahoo Finance")

# Define the symbols
tickers = {
    'Nifty 50': '^NSEI',
    'BSE Sensex': '^BSESN',
    'BSE Small Cap': '^BSESMCAP',
    'Reliance (BSE)': 'RELIANCE.BSE',
    'TCS (NSE)': 'TCS.NS'
}

# Create columns for the dashboard
cols = st.columns(len(tickers))

for i, (name, symbol) in enumerate(tickers.items()):
    try:
        ticker = yf.Ticker(symbol)
        # Use period='2d' to ensure we have the previous close for delta calculation
        data = ticker.history(period='2d')
        
        if len(data) >= 1:
            current_price = data['Close'].iloc[-1]
            # Calculate change if we have at least 2 days of data
            if len(data) > 1:
                prev_price = data['Close'].iloc[-2]
                delta = ((current_price - prev_price) / prev_price) * 100
            else:
                delta = 0
            
            # Display as a professional metric card
            cols[i].metric(label=name, value=f"₹{current_price:,.2f}", delta=f"{delta:.2f}%")
        else:
            cols[i].error(f"No data for {name}")
            
    except Exception as e:
        cols[i].error("Error")

st.divider()
st.info("Note: Data is delayed according to Yahoo Finance terms. Refresh the page to update.")
