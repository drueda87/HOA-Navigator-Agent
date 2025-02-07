import pytest
import psycopg2
import requests
from config import DB_CONFIG, API_URL, API_KEY
from db import get_zipcodes  # ✅ Import function to fetch zip codes

# ✅ Retrieve a valid zip code from the database before running the test
@pytest.fixture
def zip_code():
    zipcodes = get_zipcodes()
    assert len(zipcodes) > 0, "No zip codes found in the database!"
    print("Ran zip_code fixture")
    return zipcodes[0]  # ✅ Return the first zip code from the list

# ✅ Test API fetch with the correct parameter (zip code instead of address)
def test_api_fetch(zip_code):
    headers = {"apikey": API_KEY}
    params = {"postalCode": zip_code}  # ✅ Use zip code as the parameter
    response = requests.get(API_URL, headers=headers, params=params)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")  # ✅ Debugging output

    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, dict)
    assert "property" in data  # ✅ Adjust based on expected API response

# ✅ Test fetching properties from the database
@pytest.fixture
def setup_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    yield cursor  # Provide cursor for tests
    conn.close()  # Close connection after tests

def test_fetch_properties(setup_db):
    setup_db.execute("SELECT count(*)FROM properties ;")
    result = setup_db.fetchall()
    assert len(result) > 0, "No properties found in the database!"
