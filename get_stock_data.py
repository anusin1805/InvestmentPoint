import yfinance as yf
import pandas as pd

# Define the list of tickers you want to track
# Yahoo Finance uses specific suffixes:
# '^NSEI' = Nifty 50
# '^BSESN' = BSE Sensex
# '^BSESMCAP' = S&P BSE Small Cap
# 'RELIANCE.BSE' = Reliance Industries (BSE)
# 'TCS.NSE' = Tata Consultancy Services (NSE)

tickers = {
    'Nifty 50': '^NSEI',
    'BSE Sensex': '^BSESN',
    'BSE Small Cap': '^BSESMCAP',
    'Reliance (BSE)': 'RELIANCE.BSE'
}

print(f"{'INDEX/STOCK':<20} | {'PRICE':<10} | {'CHANGE %':<10} | {'MARKET STATUS'}")
print("-" * 60)

for name, symbol in tickers.items():
    try:
        # Fetch the ticker object
        ticker = yf.Ticker(symbol)
        
        # Get the latest market data (1 day history)
        # We use 'history' instead of 'info' because 'info' is sometimes slower or rate-limited
        data = ticker.history(period='1d')
        
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            open_price = data['Open'].iloc[-1]
            
            # Calculate percentage change (approximate for live market)
            # Note: For precise live change, you often need previous close, 
            # which yfinance provides as 'previousClose' in .info, but .history is faster.
            prev_close = ticker.info.get('previousClose', open_price)
            change_percent = ((current_price - prev_close) / prev_close) * 100
            
            print(f"{name:<20} | {current_price:<10.2f} | {change_percent:<+9.2f}% | Active")
        else:
            print(f"{name:<20} | {'N/A':<10} | {'N/A':<10} | No Data")
            
    except Exception as e:
        print(f"{name:<20} | Error fetching data: {e}")

print("-" * 60)
print("Data fetched successfully from Yahoo Finance.")