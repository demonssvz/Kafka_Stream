import streamlit as st
from pymongo import MongoClient

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['currency_db']
collection = db['exchange_rates']

st.title("Currency Exchange Dashboard")

# Fetch and display data
data = collection.find().sort("_id", -1).limit(10)
for record in data:
    st.write(record)
