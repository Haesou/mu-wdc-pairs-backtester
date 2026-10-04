from data import get_prices
from signals import compute_zscore
from backtest import run_backtest, summarize_results

HOLDING_PERIOD = 40

def strategy_b_signal(z, position, holding_period=None):
    if position is None:
        if z > 2:
            return "enter_long_MU"
        elif z < -2:
            return "enter_short_MU"
        else:
            return "hold"
    else:
        if holding_period and holding_period >= HOLDING_PERIOD:
            return "exit"
        else:
            return "hold"

if __name__ == "__main__":
    prices = get_prices()
    z = compute_zscore(prices)
    trades = run_backtest(prices, z, strategy_b_signal)
    results = summarize_results(trades)
    print(results)