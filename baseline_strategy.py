from data import get_prices
prices = get_prices()

mu_first = prices.iloc[0]['MU']
mu_last = prices.iloc[-1]['MU']
wdc_first = prices.iloc[0]['WDC']
wdc_last = prices.iloc[-1]['WDC']

mu_return = (mu_last - mu_first) / mu_first
wdc_return = (wdc_last - wdc_first) / wdc_first

buy_hold_return = (mu_return + wdc_return) / 2
print("Buy and hold return:", buy_hold_return)