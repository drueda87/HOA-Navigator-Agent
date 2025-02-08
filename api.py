import requests
from config import API_URL, API_KEY


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
    """Fetch all pages of addresses for a given zip code from the API"""
    headers = {"apikey": API_KEY}
    params = {"postalcode": zip_code, "pagesize": 500, "page": 1}
    all_properties = []

    try:
        # Initial request to determine total pages
        print(f"Requesting page {params['page']} for ZIP {zip_code}...")
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Calculate total pages based on total records and pagesize
        total = data.get("status", {}).get("total", 0)
        pagesize = params["pagesize"]
        total_pages = (total + pagesize - 1) // pagesize  # Ceiling division
        print(f"Total records: {total}, Pagesize: {pagesize}, Total pages: {total_pages}")

        # Add first page data
        properties = data.get("property", [])
        all_properties.extend(properties)
        print(f"Fetched {len(properties)} properties from page 1.")

        # Fetch remaining pages
        for page in range(2, total_pages + 1):
            params["page"] = page
            print(f"Requesting page {page} for ZIP {zip_code}...")
            response = requests.get(API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            properties = data.get("property", [])
            all_properties.extend(properties)
            print(f"Fetched {len(properties)} properties from page {page}.")

    except requests.exceptions.RequestException as e:
        print(f"API Request Failed for {zip_code}: {e}")
        return []

    print(f"Total properties fetched for ZIP {zip_code}: {len(all_properties)}")
    return all_properties
