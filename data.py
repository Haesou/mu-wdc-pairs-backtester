import yfinance as yf

# downloading stock price data on MU and WDC from yfinance
def get_prices():
    data = yf.download(["MU", "WDC"], start="2015-01-01", end="2026-09-28") 
    prices = data['Close'] # working with the price that a stock closed on in a given day

    return prices