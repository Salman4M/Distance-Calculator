import requests


API_KEY = "1aad5bd2b9bb628db5aff47b743a968f"
url = "https://api.aviationstack.com/v1/airports"
params = {"access_key": API_KEY, "limit": 100}

response = requests.get(url=url, params=params)

data = response.json()

for airport in data.get("data", []):
    print(
        airport["iata_code"],
        airport["airport_name"],
        airport["latitude"],
        airport["longitude"],
    )
