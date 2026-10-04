from data import get_prices

def run_baseline(prices):
    mu_first = prices.iloc[0]['MU']
    mu_last = prices.iloc[-1]['MU']
    wdc_first = prices.iloc[0]['WDC']
    wdc_last = prices.iloc[-1]['WDC']

    mu_return = (mu_last - mu_first) / mu_first
    wdc_return = (wdc_last - wdc_first) / wdc_first

    return (mu_return + wdc_return) / 2

if __name__ == "__main__":
    prices = get_prices()
    buy_hold_return = run_baseline(prices)
    print("Buy and hold return:", buy_hold_return)