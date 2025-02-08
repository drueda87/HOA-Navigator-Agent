import requests
from config import API_URL, API_KEY

def fetch_addresses(zip_code):
    """Fetch all pages of addresses for a given zip code from the API"""
    headers = {"apikey": API_KEY}
    params = {"postalcode": zip_code, "pagesize": 100, "page": 1}
    all_properties = []

    try:
        while True:
            response = requests.get(API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            properties = data.get("property", [])
            all_properties.extend(properties)

            # Check if there are more pages
            if "next_page" in data:  # Adjust based on API response format
                params["page"] += 1
            else:
                break
    
    except requests.exceptions.RequestException as e:
        print(f"API Request Failed for {zip_code}: {e}")
        return []

    return all_properties
