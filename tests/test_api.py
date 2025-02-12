from api import fetch_addresses
import requests
from unittest.mock import patch

def test_fetch_addresses_pagination(mocker):
    """Test that fetch_addresses calculates pages correctly and retrieves all data with pagesize 2000"""
    
    # Mock the first response with total records and first page of data (2000 properties)
    mock_response_1 = mocker.Mock()
    mock_response_1.json.return_value = {
        "status": {"total": 2500},
        "property": [{"address": "123 Main St"}] * 2000  # Simulating 2000 properties
    }
    mock_response_1.status_code = 200

    # Mock the second response for page 2 (remaining 500 properties)
    mock_response_2 = mocker.Mock()
    mock_response_2.json.return_value = {
        "status": {"total": 2500},
        "property": [{"address": "456 Elm St"}] * 500  # Simulating 500 properties
    }
    mock_response_2.status_code = 200

    # Mock requests.get to return only two responses now
    mocker.patch("requests.get", side_effect=[mock_response_1, mock_response_2])

    # Call the function
    addresses = fetch_addresses("66208")

    # ✅ Ensure function does not return None
    assert addresses is not None, "fetch_addresses returned None"
    assert isinstance(addresses, list), "fetch_addresses did not return a list"

    # ✅ Ensure total properties fetched matches expected API total
    assert len(addresses) == 2500  # Expected total
    assert addresses[:1][0]["address"] == "123 Main St"  # First page properties
    assert addresses[1999:2000][0]["address"] == "123 Main St"  # Last property of page 1
    assert addresses[2000:2001][0]["address"] == "456 Elm St"  # First property of page 2
    assert addresses[2499:2500][0]["address"] == "456 Elm St"  # Last property of page 2
