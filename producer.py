import json
import time
import random
import requests
from kafka import KafkaProducer
from datetime import datetime

# Kafka Configuration
TOPIC = 'forex_rates'
BROKER = 'localhost:9092'

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[BROKER],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Forex Pairs and INR Exchange Rates
forex_pairs = ["EUR/USD", "USD/JPY", "GBP/USD", "USD/CAD", "EUR/GBP", "USD/CHF"]
inr_pairs = ["USD/INR", "EUR/INR", "GBP/INR", "JPY/INR", "CAD/INR", "CHF/INR"]

# Function to fetch exchange rates
def fetch_forex_data():
    api_url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        rates = {}
        for pair in forex_pairs + inr_pairs:
            base, quote = pair.split("/")
            if base == "USD":
                rate = data["rates"].get(quote, 0)
            elif base in data["rates"]:
                usd_value = data["rates"].get(base, 1)
                rate = data["rates"].get(quote, 0) / usd_value
            else:
                rate = None

            # Apply ±2% fluctuation
            if rate:
                rate *= random.uniform(0.98, 1.02)  # Adding volatility

            rates[pair] = round(rate, 4) if rate else None

        return rates
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching exchange rates: {e}")
        return {pair: None for pair in forex_pairs + inr_pairs}

# Function to fetch oil price (Simulated with fluctuations)
def fetch_oil_price():
    base_price = 75.0  # Base oil price in USD per barrel
    fluctuation = random.uniform(-1, 1)  # ±1 USD fluctuation
    return round(base_price + fluctuation, 2)

print("🔄 Streaming Forex and INR Exchange Rates to Kafka...")

while True:
    rates = fetch_forex_data()
    oil_price = fetch_oil_price()

    message = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rates": rates,
        "oil_price": oil_price
    }

    producer.send(TOPIC, value=message)
    print(f"📤 Sent: {message}")

    time.sleep(5)  # Adjust frequency as needed
