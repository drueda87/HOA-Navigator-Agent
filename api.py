import requests
import time
from config import API_URL, API_KEY
from db import update_property_count


"""
def fetch_addresses(zip_code):
    """"""Fetch all pages of addresses for a given zip code from the API"""""""
    headers = {"apikey": API_KEY}
    params = {"postalcode": zip_code, "pagesize": 100, "page": 1}
    all_properties = []

    try:
        while True:
            print(f"Requesting page {params['page']} for ZIP {zip_code}...")  # Debugging output
            response = requests.get(API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            properties = data.get("property", [])
            all_properties.extend(properties)
            print(f"Fetched {len(properties)} properties from page {params['page']}")  # Debugging output

            # Check if there are more pages
            if "next_page" in data:  # Adjust based on API response format
                params["page"] += 1
            else:
                break
    
    except requests.exceptions.RequestException as e:
        print(f"API Request Failed for {zip_code}: {e}")
        return []
    print(f"Total properties fetched for ZIP {zip_code}: {len(all_properties)}")
    return all_properties
"""
def fetch_addresses(zip_code):
    """Fetch all pages of addresses for a given zip code from the API and log total property count in the database."""
    headers = {"apikey": API_KEY}
    params = {"postalcode": zip_code, "pagesize": 2000, "page": 1}
    all_properties = []

    try:
        print(f"Requesting page {params['page']} for ZIP {zip_code}...")
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # ✅ Debug: Print API response for first request
        print(f"DEBUG: Raw API response for page 1: {data}")

        total = data.get("status", {}).get("total", 0)
        print(f"Total records reported by API: {total}")

        properties = data.get("property", [])
        print(f"Fetched {len(properties)} properties from page 1.")
        all_properties.extend(properties)

        total_pages = (total + params["pagesize"] - 1) // params["pagesize"]

        for page in range(2, total_pages + 1):
            params["page"] = page
            print(f"Requesting page {page} for ZIP {zip_code}...")
            response = requests.get(API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            # ✅ Debug: Print API response for each page
            print(f"DEBUG: Raw API response for page {page}: {data}")

            properties = data.get("property", [])
            print(f"Fetched {len(properties)} properties from page {page}.")
            all_properties.extend(properties)

            time.sleep(2)  # Rate limit delay

        print(f"DEBUG: Total properties collected: {len(all_properties)}")

        update_property_count(zip_code, total)

    except requests.exceptions.RequestException as e:
        print(f"API Request Failed for {zip_code}: {e}")
        return []

    print(f"Total properties fetched for ZIP {zip_code}: {len(all_properties)}")
    return all_properties
