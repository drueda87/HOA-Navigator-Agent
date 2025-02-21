from api import fetch_addresses
from db import insert_property, update_property_count
import requests
from unittest.mock import patch

def test_fetch_addresses_pagination(mocker):
    """Test that fetch_addresses paginates correctly, inserts properties, and updates property count"""

    # Mock the first API response with total records and first page of data (2000 properties)
    mock_response_1 = mocker.Mock()
    mock_response_1.json.return_value = {
        "status": {"total": 2500},
        "property": [{"address": "123 Main St"}] * 2000  # Simulating 2000 properties
    }
    mock_response_1.status_code = 200

    # Mock the second API response for page 2 (remaining 500 properties)
    mock_response_2 = mocker.Mock()
    mock_response_2.json.return_value = {
        "status": {"total": 2500},
        "property": [{"address": "456 Elm St"}] * 500  # Simulating 500 properties
    }
    mock_response_2.status_code = 200

    # Mock `requests.get` to return two responses
    mocker.patch("requests.get", side_effect=[mock_response_1, mock_response_2])

    # Mock `insert_property` and `update_property_count`
    mock_insert_property = mocker.patch("db.insert_property")
    mock_update_property_count = mocker.patch("db.update_property_count")

    # Call the function
    fetch_addresses("66208")

    # ✅ Ensure `insert_property` was called twice (once per page)
    assert mock_insert_property.call_count == 2

    # ✅ Ensure `insert_property` was called with correct data
    first_call_args = mock_insert_property.call_args_list[0][0][0]  # First batch of properties
    second_call_args = mock_insert_property.call_args_list[1][0][0]  # Second batch of properties

    assert len(first_call_args) == 2000  # First page contains 2000 properties
    assert len(second_call_args) == 500  # Second page contains 500 properties
    assert first_call_args[0]["address"] == "123 Main St"  # First page data validation
    assert second_call_args[0]["address"] == "456 Elm St"  # Second page data validation

    # ✅ Ensure `update_property_count` was called once
    mock_update_property_count.asse
