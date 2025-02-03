import requests
from config import API_URL, API_KEY

def fetch_addresses(zip_code):
    """Fetch addresses for a given zip code from the API"""
headers = {"apikey": API_KEY}
params = {"postalcode": zip_code, "pagesize": 100}

try:
    response = requests.get(API_URL, headers = headers, params = params)
    response.raise_for_status()
    data = response.json()
    return data.get("property", []) # return list of properties
except requests.exceptions.RequestException as e:
    print(f"API Request Failed for {zip_code}: {e}")
    return []
