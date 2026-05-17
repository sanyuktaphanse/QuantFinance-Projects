import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker = "SPY"
df = yf.download(ticker, start="2010-01-01", end="2020-12-31")
df = df[["Close"]]

# Moving averages
df["MA50"] = df["Close"].rolling(window=50).mean()
df["MA200"] = df["Close"].rolling(window=200).mean()
df.dropna(inplace=True)

# Signals
df["Signal"] = 0
df.loc[df["MA50"] > df["MA200"], "Signal"] = 1
df["Position"] = df["Signal"].diff()

# Returns
df["Market_Return"] = df["Close"].pct_change()
df["Strategy_Return"] = df["Market_Return"] * df["Signal"].shift(1)
df["Cumulative_Market"] = (1 + df["Market_Return"]).cumprod()
df["Cumulative_Strategy"] = (1 + df["Strategy_Return"]).cumprod()

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.plot(df["Close"], label="SPY Price", color="gray", linewidth=1)
ax1.plot(df["MA50"], label="50-day MA", color="blue", linewidth=1)
ax1.plot(df["MA200"], label="200-day MA", color="red", linewidth=1)
ax1.scatter(df[df["Position"]==1].index, df[df["Position"]==1]["Close"], marker="^", color="green", s=100, label="Buy")
ax1.scatter(df[df["Position"]==-1].index, df[df["Position"]==-1]["Close"], marker="v", color="red", s=100, label="Sell")
ax1.legend()
ax1.set_title("SPY Price with Moving Average Crossover Signals")

ax2.plot(df["Cumulative_Market"], label="Buy & Hold", color="gray")
ax2.plot(df["Cumulative_Strategy"], label="MA Strategy", color="blue")
ax2.legend()
ax2.set_title("Strategy vs Buy & Hold Returns")

plt.tight_layout()
plt.show()