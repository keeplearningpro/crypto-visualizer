from google.colab import drive
drive.mount('/content/drive',force_remount=True)
import pandas as pd
import matplotlib.pyplot as plt
bc_file_path = '/content/drive/My Drive/bcdata/bitcoin.csv'
etc_file_path = '/content/drive/My Drive/etcdata/etherium.csv'
bc_daily_file_path = '/content/drive/My Drive/bcdata/bitcoin-daily.csv'
etc_daily_file_path = '/content/drive/My Drive/etcdata/etherium-daily.csv'

# Load datasets
btc_df = pd.read_csv(bc_file_path)
eth_df = pd.read_csv(etc_file_path)
btc_daily_df = pd.read_csv(bc_daily_file_path)
eth_daily_df = pd.read_csv(etc_daily_file_path)

# Convert month to datetime
btc_df['month'] = pd.to_datetime(btc_df['month'])
eth_df['month'] = pd.to_datetime(eth_df['month'])
btc_daily_df['transaction_date'] = pd.to_datetime(btc_daily_df['transaction_date'])
eth_daily_df['transaction_date'] = pd.to_datetime(eth_daily_df['transaction_date'])

# Calculate average fees
btc_df['avg_fee_btc'] = btc_df['total_fee_btc'] / btc_df['transaction_count']
eth_df['avg_fee_eth'] = eth_df['total_fee_eth'] / eth_df['transaction_count']

# Sorting the dates: just for ensuring
btc_daily_df.sort_values('transaction_date', inplace=True)
eth_daily_df.sort_values('transaction_date', inplace=True)

# Set common style
plt.style.use('ggplot')

# 1. Bitcoin transaction volume
plt.figure(figsize=(12, 6))
plt.plot(btc_df['month'], btc_df['transaction_count'], marker='o')
plt.title("Bitcoin Transaction Volume Over 10 Years")
plt.xlabel("Month")
plt.ylabel("Number of Transactions Per Month")
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. Bitcoin total fees
plt.figure(figsize=(12, 6))
plt.plot(btc_df['month'], btc_df['total_fee_btc'], marker='o', color='purple')
plt.title("Bitcoin Total Transaction Fees (BTC)")
plt.xlabel("Month")
plt.ylabel("Total Fees in BTC Per Month")
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot 3: Bitcoin Average Fee Per Transaction
plt.figure(figsize=(12, 6))
plt.plot(btc_df['month'], btc_df['avg_fee_btc'], marker='o', color='darkblue')
plt.title("Bitcoin Average Fee Per Transaction (BTC)")
plt.xlabel("Month")
plt.ylabel("Avg Fee (BTC)")
plt.grid(True)
plt.tight_layout()
plt.show()

# 4. Ethereum transaction volume
plt.figure(figsize=(12, 6))
plt.plot(eth_df['month'], eth_df['transaction_count'], marker='o', color='green')
plt.title("Ethereum Transaction Volume Over 10 Years")
plt.xlabel("Month")
plt.ylabel("Number of Transactions Per Month")
plt.grid(True)
plt.tight_layout()
plt.show()

# 5. Ethereum total gas fees
plt.figure(figsize=(12, 6))
plt.plot(eth_df['month'], eth_df['total_fee_eth'], marker='o', color='red')
plt.title("Ethereum Total Gas Fees (ETH)")
plt.xlabel("Month")
plt.ylabel("Total Gas Fees in ETH Per Month")
plt.grid(True)
plt.tight_layout()
plt.show()

# 6: Ethereum Average Fee Per Transaction
plt.figure(figsize=(12, 6))
plt.plot(eth_df['month'], eth_df['avg_fee_eth'], marker='o', color='darkred')
plt.title("Ethereum Average Fee Per Transaction (ETH)")
plt.xlabel("Month")
plt.ylabel("Avg Fee (ETH)")
plt.grid(True)
plt.tight_layout()
plt.show()

# 7. Compare BTC vs ETH Average Transaction Fees
plt.figure(figsize=(12, 6))
plt.plot(btc_df['month'], btc_df['avg_fee_btc'], label='Bitcoin Avg Fee (BTC)', color='blue')
plt.plot(eth_df['month'], eth_df['avg_fee_eth'], label='Ethereum Avg Fee (ETH)', color='orange')
plt.title("BTC vs ETH Average Transaction Fee Comparison")
plt.xlabel("Month")
plt.ylabel("Avg Fee (BTC / ETH)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 8. Plot comparison
plt.figure(figsize=(14, 7))
plt.plot(btc_daily_df['transaction_date'], btc_daily_df['daily_transaction_count'], label='Bitcoin', color='blue', alpha=0.7)
plt.plot(eth_daily_df['transaction_date'], eth_daily_df['daily_transaction_count'], label='Ethereum', color='orange', alpha=0.7)

plt.title("Daily Transactions: Bitcoin vs Ethereum")
plt.xlabel("Date")
plt.ylabel("Number of Transactions")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
