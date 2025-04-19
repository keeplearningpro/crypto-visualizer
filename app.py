import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Config ---
st.set_page_config(page_title="Crypto Visualizer", layout="centered")
st.title("📊 Cryptocurrency Transaction Visualizer")

st.markdown("""
Welcome! This dashboard pulls live cryptocurrency data (Bitcoin and Ethereum) from GitHub and helps you:
- Compare **transaction volumes**
- Examine **transaction fee trends**
- Understand **network cost efficiency**

Use the sidebar to customize the number of years to visualize.
""")

# --- Sidebar Control ---
years = st.sidebar.selectbox("Select time range (years):", [10, 5, 2])
st.sidebar.markdown("Choose how many years of data to analyze.")

# --- Load data from GitHub ---
@st.cache_data
def load_data():
    btc_url = "https://raw.githubusercontent.com/keeplearningpro/crypto-visualizer/main/data/bitcoin.csv"
    eth_url = "https://raw.githubusercontent.com/keeplearningpro/crypto-visualizer/main/data/ethereum.csv"

    btc_df = pd.read_csv(btc_url)
    eth_df = pd.read_csv(eth_url)

    btc_df['month'] = pd.to_datetime(btc_df['month'])
    eth_df['month'] = pd.to_datetime(eth_df['month'])

    # Calculate average fee per transaction
    btc_df['avg_fee'] = btc_df['total_fee_btc'] / btc_df['transaction_count']
    eth_df['avg_fee'] = eth_df['total_fee_eth'] / eth_df['transaction_count']

    return btc_df, eth_df

btc_df, eth_df = load_data()

# --- Filter data ---
cutoff = pd.Timestamp.today() - pd.DateOffset(years=years)
btc_df = btc_df[btc_df['month'] >= cutoff]
eth_df = eth_df[eth_df['month'] >= cutoff]

# --- Plot 1: Transaction Volume ---
st.subheader("📈 Monthly Transaction Volume")
fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(btc_df['month'], btc_df['transaction_count'], label='Bitcoin', marker='o')
ax1.plot(eth_df['month'], eth_df['transaction_count'], label='Ethereum', marker='o')
ax1.set_xlabel("Month")
ax1.set_ylabel("Transactions")
ax1.set_title("Monthly Transaction Count")
ax1.legend()
st.pyplot(fig1)

# --- Plot 2: Total Transaction Fees ---
st.subheader("💸 Monthly Total Transaction Fees")
fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(btc_df['month'], btc_df['total_fee_btc'], label='Bitcoin Fees (BTC)', marker='o')
ax2.plot(eth_df['month'], eth_df['total_fee_eth'], label='Ethereum Fees (ETH)', marker='o')
ax2.set_xlabel("Month")
ax2.set_ylabel("Fees")
ax2.set_title("Total Monthly Fees")
ax2.legend()
st.pyplot(fig2)

# --- Plot 3: Average Fee per Transaction ---
st.subheader("🧮 Average Fee per Transaction")
fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.plot(btc_df['month'], btc_df['avg_fee'], label='Bitcoin Avg Fee (BTC)', marker='o')
ax3.plot(eth_df['month'], eth_df['avg_fee'], label='Ethereum Avg Fee (ETH)', marker='o')
ax3.set_xlabel("Month")
ax3.set_ylabel("Avg Fee")
ax3.set_title("Average Fee per Transaction")
ax3.legend()
st.pyplot(fig3)

st.markdown("---")
st.markdown("📌 [GitHub Repo](https://github.com/your-username/your-repo)")
