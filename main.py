import yfinance as yf
import numpy as np
from statsmodels.tsa.stattools import adfuller

# downloading stock price data on MU and WDC from yfinance
data = yf.download(["MU", "WDC"], start="2015-01-01", end="2026-09-28") 

# working with the price that a stock closed on in a given day
prices = data['Close'] 

# log ratio is symmetric when increasing by 2x and decreasing by 2x. a simple ratio is not symmetric
log_ratio = np.log(prices['MU'] / prices['WDC']) 

log_ratio_early = log_ratio.loc["2015-01-01":"2022-12-31"]
log_ratio_late = log_ratio.loc["2023-01-01":"2026-09-28"]

window = 60

# rolling mean calculates the average log ratio over the past n days, n being 60 in this case
rolling_mean = log_ratio.rolling(window).mean()
# rolling std calculates how spread out the log ratio values are over the past 60 days
rolling_std = log_ratio.rolling(window).std()

# z_score gives you how many standard deviations today's log ratio is from the 60-day mean log ratio
z_score = (log_ratio - rolling_mean) / rolling_std

print(z_score.describe())
print(z_score.tail(10))

result_early, result_late = adfuller(log_ratio_early), adfuller(log_ratio_late)

print("Early ADF Statistic:", result_early[0])
print("Early p-value:", result_early[1])
print("Late ADF Statistic:", result_late[0])
print("Late p-value:", result_late[1])