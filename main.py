import yfinance as yf
import numpy as np

data = yf.download(["MU", "WDC"], start="2015-01-01", end="2026-09-28")

prices = data['Close']

log_ratio = np.log(prices['MU'] / prices['WDC'])

window = 60

rolling_mean = log_ratio.rolling(window).mean()
rolling_std = log_ratio.rolling(window).std()

z_score = (log_ratio - rolling_mean) / rolling_std

print(z_score.describe())
print(z_score.tail(10))