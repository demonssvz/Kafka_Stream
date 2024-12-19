from pymongo import MongoClient

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['currency_db']
collection = db['exchange_rates']

# Save data to MongoDB
for message in consumer:
    data = message.value
    print("Received message:", data)
    collection.insert_one(data)  # Save to MongoDB
