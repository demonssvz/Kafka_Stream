from kafka import KafkaConsumer
import json

# Kafka Configuration
TOPIC = 'currency_exchange'
BROKER = 'localhost:9092'

# Kafka Consumer Setup
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[BROKER],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='currency_consumer_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # JSON deserialization
)

print("Listening for messages from Kafka...")

for message in consumer:
    data = message.value
    print("Received message:", data)
    # Process the data (e.g., calculate trends, thresholds, etc.)
