import pandas as pd

trades = pd.read_csv(r"C:\Users\Raj Singh\Downloads\historical_data.csv")
sentiment = pd.read_csv(r"C:\Users\Raj Singh\Downloads\fear_greed_index.csv")

trades['Timestamp IST'] = pd.to_datetime(trades['Timestamp IST'], format='%d-%m-%Y %H:%M', errors='coerce')
sentiment['date'] = pd.to_datetime(sentiment['date'], errors='coerce')
trades['date'] = trades['Timestamp IST'].dt.date
sentiment['date'] = sentiment['date'].dt.date
merged_df = pd.merge(trades, sentiment[['date', 'classification', 'value']], on='date', how='left')
print(merged_df[['Account', 'Timestamp IST', 'Closed PnL', 'classification', 'value']].head())

avg_pnl_by_sentiment = merged_df.groupby('classification')['Closed PnL'].mean().sort_values(ascending=False)
print(avg_pnl_by_sentiment)

trade_counts = merged_df['classification'].value_counts()
print(trade_counts)

if 'Leverage' in merged_df.columns:
    avg_leverage = merged_df.groupby('classification')['Leverage'].mean()
    print(avg_leverage)


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
sns.boxplot(data=merged_df, x='classification', y='Closed PnL')
plt.title('Distribution of Trader PnL by Market Sentiment')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 4))
sns.countplot(data=merged_df, x='classification', order=merged_df['classification'].value_counts().index)
plt.title('Number of Trades by Market Sentiment')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()
