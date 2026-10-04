from data import get_prices
from signals import compute_zscore
from backtest import run_backtest, summarize_results

def strategy_a_signal(z, position, holding_period=None):
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

if __name__ == "__main__":
    prices = get_prices()
    z = compute_zscore(prices)
    trades = run_backtest(prices, z, strategy_a_signal)
    results = summarize_results(trades)
    print(results)