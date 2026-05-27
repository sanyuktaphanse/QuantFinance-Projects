import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "NVDA", "JPM", "V", "UNH", "XOM",
    "JNJ", "WMT", "PG", "MA", "HD",
    "BAC", "ABBV", "PFE", "COST", "NFLX"
]

print("Downloading data...")
df = yf.download(tickers, start="2022-01-01", end="2024-01-01")["Close"]

momentum = df.pct_change(252).iloc[-1]
momentum = momentum.dropna()
momentum = momentum.sort_values(ascending=False)
top5 = momentum.head(5)

print("\nMomentum scores (best to worst):")
print(momentum.round(2))
print("\nTop 5 momentum stocks:")
print(top5.round(2))

plt.figure(figsize=(12, 5))
colors = ["green" if x > 0 else "red" for x in momentum]
plt.bar(momentum.index, momentum.values * 100, color=colors)
plt.axhline(0, color="black", linewidth=0.8)
plt.title("12-Month Momentum Scores by Stock")
plt.ylabel("Return (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# BACKTEST
print("\nRunning backtest...")
df_bt = yf.download(tickers, start="2019-01-01", end="2024-01-01")["Close"]
monthly = df_bt.resample("ME").last().pct_change()

portfolio_returns = []
dates = []

for i in range(12, len(monthly)):
    past_12 = df_bt.resample("ME").last().iloc[i-12:i].pct_change().add(1).prod().sub(1)
    top5_bt = past_12.nlargest(5).index.tolist()
    this_month_return = monthly.iloc[i][top5_bt].mean()
    portfolio_returns.append(this_month_return)
    dates.append(monthly.index[i])

results = pd.Series(portfolio_returns, index=dates)
cumulative_strategy = (1 + results).cumprod()

spy = yf.download("SPY", start="2019-01-01", end="2024-01-01")["Close"]
spy_monthly = spy.resample("ME").last().pct_change()
spy_monthly = spy_monthly.loc[results.index]
cumulative_spy = (1 + spy_monthly).cumprod()

plt.figure(figsize=(12, 5))
plt.plot(cumulative_strategy, label="Momentum Top 5", color="blue")
plt.plot(cumulative_spy, label="SPY Buy and Hold", color="gray")
plt.title("Momentum Strategy vs SPY (2019-2024)")
plt.ylabel("Growth of $1")
plt.legend()
plt.tight_layout()
plt.show()

final_strat = cumulative_strategy.iloc[-1]
final_spy = cumulative_spy.iloc[-1]
print(f"\nMomentum strategy turned $1 into ${final_strat:.2f}")
print(f"SPY buy and hold turned $1 into ${final_spy:.2f}")







