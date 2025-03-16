import json
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from kafka import KafkaConsumer
from collections import deque

# Kafka Configuration
TOPIC = 'multi_currency_inr'
BROKER = 'localhost:9092'

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[BROKER],
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

 
window_size = 50  # Number of recent data points to display
currencies = ["USD", "EUR", "GBP", "JPY"]
data_store = {currency: deque(maxlen=window_size) for currency in currencies}
timestamps = deque(maxlen=window_size)

# Streamlit UI
st.title("📈 Multi-Currency INR Exchange Rate Tracker")
st.write("Real-time visualization of INR exchange rates with USD, EUR, GBP, and JPY.")

data_list = []

# Kafka Message Listener
for message in consumer:
    data = message.value
    timestamps.append(data["timestamp"])
    data_list.append(data)

    # Update Currency Data
    for currency, rate in data["rates"].items():
        data_store[currency].append(rate)
    
    # Convert data to Pandas DataFrame for easy processing
    df = pd.DataFrame({currency: list(data_store[currency]) for currency in currencies}, index=list(timestamps))
    df['timestamp'] = pd.to_datetime(df.index)
    df.set_index('timestamp', inplace=True)

    # Moving Averages
    df['SMA_5'] = df.mean(axis=1).rolling(window=5).mean()
    df['SMA_20'] = df.mean(axis=1).rolling(window=20).mean()

    # Volatility Calculation
    df['volatility'] = df.mean(axis=1).rolling(window=5).std()

    # 1 Exchange Rate Trends
    st.subheader("📊 Exchange Rate Trends")
    fig, axs = plt.subplots(len(currencies), 1, figsize=(10, 8), sharex=True)

    for i, currency in enumerate(currencies):
        axs[i].plot(df.index, df[currency], label=f"INR to {currency}", marker="o", linestyle="-")
        axs[i].legend()
        axs[i].set_ylabel("Exchange Rate")
        axs[i].grid(True)

    axs[-1].set_xlabel("Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # 2 Latest Exchange Rates
    st.subheader("📊 Latest Exchange Rates")
    latest_rates = {currency: df[currency].iloc[-1] for currency in currencies}
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(latest_rates.keys(), latest_rates.values(), color=["blue", "green", "red", "purple"])
    ax.set_ylabel("Exchange Rate")
    ax.set_title("Latest INR Exchange Rates")
    st.pyplot(fig)

    # Moving Average for Trend Analysis
    st.subheader("📈 Moving Average Analysis")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['SMA_5'], label='5-Point SMA', linestyle="--", color='orange')
    ax.plot(df.index, df['SMA_20'], label='20-Point SMA', linestyle="--", color='blue')
    ax.set_xlabel("Time")
    ax.set_ylabel("Exchange Rate")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

    # **4️⃣ Volatility Analysis**
    st.subheader("⚡ Exchange Rate Volatility")
    st.line_chart(df[['volatility']], use_container_width=True)

    # **5️⃣ Exchange Rate Statistics**
    st.subheader("📋 Exchange Rate Statistics")
    rate_summary = {
        "Currency": [],
        "Min Rate": [],
        "Max Rate": [],
        "Avg Rate": []
    }

    for currency in currencies:
        rate_summary["Currency"].append(currency)
        rate_summary["Min Rate"].append(round(df[currency].min(), 4))
        rate_summary["Max Rate"].append(round(df[currency].max(), 4))
        rate_summary["Avg Rate"].append(round(df[currency].mean(), 4))

    st.table(pd.DataFrame(rate_summary))

 
    time.sleep(1)
 

