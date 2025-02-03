from db import insert_property
from api import fetch_addresses

def process_zipcode(zip_code):
    """Fetch and insert propery data from a given ZIP code"""
    print(f"Fetching addresses for ZIP code: {zip_code}")
    properties = fetch_addresses(zip_code)

    if properties:
        insert_property(properties)
        print(f"Inserted {len(properties)} properties for ZIP code: {zip_code}")
    else:
         print(f"No properties found for ZIP Code: {zip_code}")