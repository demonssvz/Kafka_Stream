from kafka import KafkaProducer
import requests
import json
import time

# Kafka Configuration
TOPIC = 'currency_exchange'
BROKER = 'localhost:9092'

# API Configuration
API_KEY = 'f94e833a26fc2e1026f62c43b6f04c6a'  # Replace with your API key
API_URL = f"http://data.fixer.io/api/latest?access_key={API_KEY}"  # Example: Fixer API

# Kafka Producer Setup
producer = KafkaProducer(
    bootstrap_servers=[BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # JSON serialization
)

def fetch_and_stream():
    while True:
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                print("Streaming data to Kafka:", data)
                producer.send(TOPIC, value=data)
                producer.flush()
            else:
                print("Error fetching data:", response.status_code)
            time.sleep(10)  # Fetch data every 10 seconds
        except Exception as e:
            print("Error:", e)
            time.sleep(10)

if __name__ == "__main__":
    print("Starting to stream data into Kafka...")
    fetch_and_stream()
