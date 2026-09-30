from data import get_prices
from signals import compute_log_ratio, compute_zscore, run_adf_test

prices = get_prices()

z_score = compute_zscore(prices)
adf_score = run_adf_test(prices)

print(z_score.describe())
print(z_score.tail(10))

print("ADF Statistic:", adf_score[0])
print("p-value:", adf_score[1])