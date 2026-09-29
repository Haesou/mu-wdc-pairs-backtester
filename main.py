import yfinance as yf

# download() returns a DataFrame with a DatetimeIndex (the dates are the row labels, not a normal column)
mu_data = yf.download("MU", start="2015-01-01", end="2026-09-28")

print(mu_data.head())      # look at the first 5 rows
print(mu_data.columns)     # see what columns you got (Open, High, Low, Close, Adj Close, Volume - though newer yfinance versions sometimes merge Close/Adj Close depending on the `auto_adjust` parameter)
print(mu_data.shape)       # (num_rows, num_columns) - like checking len() but for 2 dimensions