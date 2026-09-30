from data import get_prices
from signals import compute_zscore


def strategy_a_signal(z, position):
    if position is None:
        if z > 2:
            return "enter_short_MU"
        elif z < -2:
            return "enter_long_MU"
        else:
            return "hold"
    else:
        if position == "short_MU" and z <= 0:
            return "exit"
        elif position == "long_MU" and z >= 0:
            return "exit"
        else:
            return "hold"

prices = get_prices()
z = compute_zscore(prices)

trades = []

position = None
en_date = None
ex_date = None

mu_entry = None
wdc_entry = None

for date, row in prices.iterrows():
    mu_price = row['MU']
    wdc_price = row['WDC']
    signal = strategy_a_signal(z[date], position)

    if position is None:
        if signal == "enter_short_MU":
            position = "short_MU"
            en_date = date

            mu_entry, wdc_entry = mu_price, wdc_price
        elif signal == "enter_long_MU":
            position = "long_MU"
            en_date = date

            mu_entry, wdc_entry = mu_price, wdc_price
    else:
        if signal == "exit":
            trades.append({
                "entry_date": en_date,
                "exit_date": date,
                "direction": position,
                "mu_entry": mu_entry,
                "wdc_entry": wdc_entry,
                "mu_exit": mu_price,
                "wdc_exit": wdc_price
            })
            position = None
            en_date = None

if position:
    last_date = prices.index[-1]
    last_mu = prices.iloc[-1]['MU']
    last_wdc = prices.iloc[-1]['WDC']
    
    trades.append({
        "entry_date": en_date,
        "exit_date": last_date,
        "direction": position,
        "mu_entry": mu_entry,
        "wdc_entry": wdc_entry,
        "mu_exit": last_mu,
        "wdc_exit": last_wdc
    })

print(len(trades))
print(trades[0])