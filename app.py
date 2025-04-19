import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

# ---- PAGE SETUP ---- #
st.set_page_config(page_title="Crypto Transactions Blog & Visualizer", layout="centered")
st.title("📊 Cryptocurrency Analytics Blog")

st.markdown("""
Welcome to this interactive blog on **Cryptocurrency Transaction Volumes and Fees**. In this post, we explore:
- The evolution of transaction activity on **Bitcoin** and **Ethereum**
- How transaction **fees** have fluctuated over time
- What these trends imply about **network congestion**, **adoption**, and **scalability**

Use the interactive visualizer below to generate custom plots for **2, 5, or 10 years** of data directly fetched from **Google BigQuery**.
""")

# ---- SIDEBAR CONTROLS ---- #
year_range = st.sidebar.selectbox("Select data range (years):", [10, 5, 2], index=0)
st.sidebar.markdown("Choose how many years of data to include")

# ---- BIGQUERY SETUP ---- #
# Load your service account credentials (make sure to keep them safe and secure)
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# ---- QUERY DATA FROM BIGQUERY ---- #
def load_btc_eth_data(years):
    query_template = """
        SELECT
          FORMAT_DATE('%Y-%m', DATE(block_timestamp)) AS month,
          COUNT(*) AS transaction_count,
          SUM(CAST({fee_column} AS FLOAT64)) / POWER(10, {divider}) AS total_fee
        FROM `{table}`
        WHERE DATE(block_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL {years} YEAR)
        GROUP BY month
        ORDER BY month
    """

    btc_query = query_template.format(
        fee_column="fee",
        divider="8",
        table="bigquery-public-data.crypto_bitcoin.transactions",
        years=years
    )

    eth_query = query_template.format(
        fee_column="gas_price * gas",
        divider="18",
        table="bigquery-public-data.crypto_ethereum.transactions",
        years=years
    )

    btc_df = client.query(btc_query).to_dataframe()
    eth_df = client.query(eth_query).to_dataframe()

    btc_df['month'] = pd.to_datetime(btc_df['month'])
    eth_df['month'] = pd.to_datetime(eth_df['month'])
    btc_df['avg_fee'] = btc_df['total_fee'] / btc_df['transaction_count']
    eth_df['avg_fee'] = eth_df['total_fee'] / eth_df['transaction_count']

    return btc_df, eth_df

btc_df, eth_df = load_btc_eth_data(year_range)

# ---- VISUALIZATIONS ---- #
st.header("📈 Transaction Volume Over Time")
fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(btc_df['month'], btc_df['transaction_count'], label='Bitcoin', marker='o')
ax1.plot(eth_df['month'], eth_df['transaction_count'], label='Ethereum', marker='o')
ax1.set_title("Monthly Transaction Volume")
ax1.set_xlabel("Month")
ax1.set_ylabel("Transactions")
ax1.legend()
st.pyplot(fig1)

st.header("💸 Total Transaction Fees")
fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(btc_df['month'], btc_df['total_fee'], label='Bitcoin Fees (BTC)', marker='o')
ax2.plot(eth_df['month'], eth_df['total_fee'], label='Ethereum Fees (ETH)', marker='o')
ax2.set_title("Monthly Total Fees")
ax2.set_xlabel("Month")
ax2.set_ylabel("Fees")
ax2.legend()
st.pyplot(fig2)

st.header("🧮 Average Fee per Transaction")
fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.plot(btc_df['month'], btc_df['avg_fee'], label='Bitcoin Avg Fee', marker='o')
ax3.plot(eth_df['month'], eth_df['avg_fee'], label='Ethereum Avg Fee', marker='o')
ax3.set_title("Average Transaction Fee")
ax3.set_xlabel("Month")
ax3.set_ylabel("Fee per Transaction")
ax3.legend()
st.pyplot(fig3)

st.markdown("---")
st.markdown("\nThis blog was built using [Streamlit](https://streamlit.io/) and connects live to Google BigQuery for real-time blockchain data.")

