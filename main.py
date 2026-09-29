import yfinance as yf

data = yf.download(["MU", "WDC"], start="2015-01-01", end="2026-09-28")
print(data.columns)
print(data.shape)
print(data['Close'].head())

prices = data['Close']

print(prices.isna().sum())
print(prices.index.min(), prices.index.max())


#prices.to_csv("data/mu_wdc_prices.csv")