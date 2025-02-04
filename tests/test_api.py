from api import fetch_addresses
import requests
from unittest.mock import patch

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
