import numpy as np
from statsmodels.tsa.stattools import adfuller

# We use log ratio because it's symmetric when increasing by 2x and decreasing by 2x. A simple ratio is not symmetric.
def compute_log_ratio(prices):

    return np.log(prices['MU'] / prices['WDC'])

# z_score gives you how many standard deviations today's log ratio is from the 60-day mean log ratio.
def compute_zscore(prices, window=60):
    log_ratio = compute_log_ratio(prices)
    rolling_mean = log_ratio.rolling(window).mean()
    rolling_std = log_ratio.rolling(window).std()
    z_score = (log_ratio - rolling_mean) / rolling_std

    return z_score

def run_adf_test(prices):
    log_ratio = compute_log_ratio(prices)
    result = adfuller(log_ratio)

    return result