# import json
# import pandas as pd
# from kafka import KafkaConsumer

# TOPIC = 'multi_currency_inr'
# BROKER = 'localhost:9092'

# # Initialize Kafka Consumer
# consumer = KafkaConsumer(
#     TOPIC,
#     bootstrap_servers=[BROKER],
#     auto_offset_reset='latest',
#     enable_auto_commit=True,
#     group_id='currency_stream',
#     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
# )

# print("🟢 Listening for currency exchange data from Kafka...")

# data_list = []

# for message in consumer:
#     data = message.value
#     timestamp = data["timestamp"]
#     rates = data["rates"]

#     # Add data to list
#     record = {"timestamp": timestamp, **rates}
#     data_list.append(record)

#     # Save data to CSV
#     df = pd.DataFrame(data_list)
#     df.to_csv("currency_data.csv", index=False)

#     print(f"✅ Saved {len(df)} records to currency_data.csv")


import json
import time
import pandas as pd
import numpy as np
from kafka import KafkaConsumer
from collections import deque

# Kafka Configuration
TOPIC = 'forex_rates'
BROKER = 'localhost:9092'

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[BROKER],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='currency_stream',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Forex Pairs
forex_pairs = ["EUR/USD", "USD/JPY", "GBP/USD", "USD/CAD", "EUR/GBP", "USD/CHF"]
inr_pairs = ["USD/INR", "EUR/INR", "GBP/INR", "JPY/INR", "CAD/INR", "CHF/INR"]

# CSV File Storage
csv_file = "forex_data.csv"

print("🛜 Kafka Consumer Running...")

while True:
    for message in consumer:
        data = message.value
        timestamp = data["timestamp"]
        oil_price = data["oil_price"]
        rates = data["rates"]

        # Convert to DataFrame
        row = {"timestamp": timestamp, "oil_price": oil_price}
        row.update(rates)

        # Append to CSV
        df = pd.DataFrame([row])
        df.to_csv(csv_file, mode='a', header=not pd.io.common.file_exists(csv_file), index=False)

        print(f"📥 Received & Stored: {row}")
        
    time.sleep(1)  # Adjust as needed
