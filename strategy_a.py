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


def calculate_pnl(trade):
    if trade["direction"] == "short_MU":
        leg1 = (trade["mu_entry"] - trade["mu_exit"]) / trade["mu_entry"]
        leg2 = (trade["wdc_exit"] - trade["wdc_entry"]) / trade["wdc_entry"]
    else:
        leg1 = (trade["mu_exit"] - trade["mu_entry"]) / trade["mu_entry"]
        leg2 = (trade["wdc_entry"] - trade["wdc_exit"]) / trade["wdc_entry"]

    return (leg1 + leg2) / 2

pnls = []
for trade in trades:
    pnl = calculate_pnl(trade)
    trade["pnl"] = pnl
    pnls.append(pnl)

total_growth = 1

for pnl in pnls:
    total_growth = total_growth * (1 + pnl)

total_return = total_growth - 1
print("total return:", total_return)

wins = [p for p in pnls if p > 0]
win_rate = len(wins) / len(pnls)
print("Win rate:", win_rate)

losses = [p for p in pnls if p <= 0]

avg_win = sum(wins) / len(wins)
avg_loss = sum(losses) / len(losses)
print("Average win:", avg_win)
print("Average loss:", avg_loss)
