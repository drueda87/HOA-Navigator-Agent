from api import fetch_addresses
import requests
from unittest.mock import patch

"""
def test_fetch_addresses_success(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"property": [{"address": "123 Main St"}]}
    mock_response.status_code = 200
    mocker.patch("requests.get", return_value=mock_response)

    addresses = fetch_addresses("66213")
    assert isinstance(addresses, list)
    assert addresses[0]["address"] == "123 Main St"

def test_fetch_addresses_failure(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("API error")
    mocker.patch("requests.get", return_value=mock_response)

    addresses = fetch_addresses("66213")
    assert addresses == []  # Expecting an empty list if API fails
"""

"""
def test_fetch_addresses_pagination(mocker):
    """"Test that fetch_addresses retrieves multiple pages of data"""""
    mock_response_1 = mocker.Mock()
    mock_response_1.json.return_value = {
        "property": [{"address": "123 Main St"}],
        "next_page": 2  # Simulating pagination
    }
    mock_response_1.status_code = 200

    mock_response_2 = mocker.Mock()
    mock_response_2.json.return_value = {
        "property": [{"address": "456 Elm St"}]
    }
    mock_response_2.status_code = 200

    # Mock the requests.get() function to return different responses for each call
    mocker.patch("requests.get", side_effect=[mock_response_1, mock_response_2])

    addresses = fetch_addresses("66213")
    
    assert isinstance(addresses, list)
    assert len(addresses) == 2  # Expecting two addresses from two pages
    assert addresses[0]["address"] == "123 Main St"
    assert addresses[1]["address"] == "456 Elm St"
"""


def test_fetch_addresses_pagination(mocker):
    """Test that fetch_addresses calculates pages and retrieves all data"""
    # Mock the first response with total records and first page of data
    mock_response_1 = mocker.Mock()
    mock_response_1.json.return_value = {
        "status": {"total": 2500},
        "property": [{"address": "123 Main St"}] * 500  # Simulating 500 properties
    }
    mock_response_1.status_code = 200

    # Mock subsequent responses for pages 2-5
    mock_response_2 = mocker.Mock()
    mock_response_2.json.return_value = {
        "status": {"total": 2500},
        "property": [{"address": "456 Elm St"}] * 500  # Page 2
    }
    mock_response_2.status_code = 200

    mock_response_3 = mocker.Mock()
    mock_response_3.json.return_value = {
        "status": {"total": 2500},
        "property": [{"address": "789 Oak St"}] * 500  # Page 3
    }
    mock_response_3.status_code = 200

    mock_response_4 = mocker.Mock()
    mock_response_4.json.return_value = {
        "status": {"total": 2500},
        "property": [{"address": "135 Pine St"}] * 500  # Page 4
    }
    mock_response_4.status_code = 200

    mock_response_5 = mocker.Mock()
    mock_response_5.json.return_value = {
        "status": {"total": 2500},
        "property": [{"address": "246 Cedar St"}] * 500  # Page 5
    }
    mock_response_5.status_code = 200

    # Mock requests.get to return 5 responses
    mocker.patch("requests.get", side_effect=[
        mock_response_1, mock_response_2, mock_response_3, mock_response_4, mock_response_5
    ])

    # Call the function
    addresses = fetch_addresses("66208")

    # Assert that all properties from all pages were retrieved
    assert len(addresses) == 2500  # Total properties fetched
    assert addresses[:1][0]["address"] == "123 Main St"  # First page
    assert addresses[500:501][0]["address"] == "456 Elm St"  # Second page
    assert addresses[1000:1001][0]["address"] == "789 Oak St"  # Third page
    assert addresses[1500:1501][0]["address"] == "135 Pine St"  # Fourth page
    assert addresses[2000:2001][0]["address"] == "246 Cedar St"  # Fifth page
