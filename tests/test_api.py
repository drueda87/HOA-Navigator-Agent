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


def test_fetch_addresses_pagination(mocker):
    """Test that fetch_addresses retrieves multiple pages of data"""
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
