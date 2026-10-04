def run_backtest(prices, z, signal_fn):
    trades = []
    position = None
    en_date = None
    mu_entry = None
    wdc_entry = None

    for date, row in prices.iterrows():
        mu_price = row['MU']
        wdc_price = row['WDC']

        if en_date:
            holding_period = (date - en_date).days
        else:
            holding_period = None

        signal = signal_fn(z[date], position, holding_period)

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

    return trades


def calculate_pnl(trade):
    if trade["direction"] == "short_MU":
        leg1 = (trade["mu_entry"] - trade["mu_exit"]) / trade["mu_entry"]
        leg2 = (trade["wdc_exit"] - trade["wdc_entry"]) / trade["wdc_entry"]
    else:
        leg1 = (trade["mu_exit"] - trade["mu_entry"]) / trade["mu_entry"]
        leg2 = (trade["wdc_entry"] - trade["wdc_exit"]) / trade["wdc_entry"]
    return (leg1 + leg2) / 2


def summarize_results(trades):
    pnls = []
    for trade in trades:
        pnl = calculate_pnl(trade)
        trade["pnl"] = pnl
        pnls.append(pnl)

    total_growth = 1
    for pnl in pnls:
        total_growth = total_growth * (1 + pnl)
    total_return = total_growth - 1

    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p <= 0]
    win_rate = len(wins) / len(pnls)
    avg_win = sum(wins) / len(wins) if wins else 0
    avg_loss = sum(losses) / len(losses) if losses else 0

    return {
        "total_return": total_return,
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "num_trades": len(trades)
    }