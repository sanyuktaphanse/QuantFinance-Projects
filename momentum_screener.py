import yfinance as yf
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

#20 big S&P 500 stocks
tickers= [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META",
     "NVDA", "JPM", "V", "UNH", "XOM",  
     "JNJ", "WMT", "PG", "MA", "HD",
     "BAC", "ABBV", "PFE", "COST", "NFLX"
 
]
#Download 2 years of data 
print("Downloading data...")
df=yf.download(tickers, start= "2022-01-01", end="2024-01-01")["Close"]

# Compute a 12-month momentum curve for each stock 
#Momentum= return over the past 252 days 
momentum= df.pct_change(252).iloc[-1]
momentum=momentum.dropna()
momentum=momentum.sort_values(ascending=False)
top5=momentum.head(5)

print("\nMomentum scores (best to worst):")
print(momentum.round(2))

#Pick top 5
print("\nTop 5 momentum stocks:")
print(top5.round(2))

#Plot momentum scores 
plt.figure(figsize=(12, 5))
colors= ["green" if x>0 else "red" for x in momentum]
plt.bar(momentum.index, momentum.values * 100, color=colors)
plt.axhline(0,color="black", linewidth=0.8)
plt.title("12-Month Momentum Scores by Stock")
plt.ylabel("Return(%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

