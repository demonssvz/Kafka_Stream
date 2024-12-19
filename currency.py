import requests

# API URL and Key
API_KEY = "f94e833a26fc2e1026f62c43b6f04c6a"
url = f"http://data.fixer.io/api/latest?access_key={API_KEY}"

# Fetch the data
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print("Currency Exchange Rates:", data)
else:
    print("Error fetching data:", response.status_code)
