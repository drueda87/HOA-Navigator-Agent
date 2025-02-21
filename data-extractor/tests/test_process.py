from process import process_zipcode
from unittest.mock import patch

"""
@patch("process.fetch_addresses", return_value=[{"address": "123 Main St"}])
@patch("process.insert_property")
def test_process_zipcode_success(mock_insert, mock_fetch):
    process_zipcode("66213")
    mock_fetch.assert_called_once_with("66213")
    mock_insert.assert_called_once()

@patch("process.fetch_addresses", return_value=[])
@patch("process.insert_property")
def test_process_zipcode_no_data(mock_insert, mock_fetch):
    process_zipcode("66213")
    mock_fetch.assert_called_once()
    mock_insert.assert_not_called()  # Should not insert anything if no properties found
"""



@patch("process.fetch_addresses", return_value=[
    {"address": "123 Main St"},
    {"address": "456 Elm St"}
])
@patch("process.insert_property")
def test_process_zipcode_pagination(mock_insert, mock_fetch):
    """Test process_zipcode inserts multiple pages of property data"""
    process_zipcode("66213")
    mock_fetch.assert_called_once_with("66213")
    mock_insert.assert_called_once()
    assert mock_insert.call_args[0][0] == [
        {"address": "123 Main St"},
        {"address": "456 Elm St"}
    ]  # Ensure all addresses are passed to insert_property
