import pytest
from unittest.mock import patch, MagicMock
from db import get_zipcodes, insert_property

def test_get_zipcodes():
    zipcodes = get_zipcodes()
    assert isinstance(zipcodes, list)  # Should return a list
    assert all(isinstance(z, str) for z in zipcodes)  # Ensure all items are strings

@pytest.fixture
def sample_properties():
    """sample property data for testing"""
    return [
        {
            "identifier": {"attomId": "123", "fips": "456", "apn": "789"},
            "address": {
                "line1": "123 Main St",
                "line2": "",
                "locality": "Overland Park",
                "countrySubd": "KS",
                "postal1": "66212",
                "postal2": "",
                "postal3": "",
                "country": "US",
                "matchCode": "Exact",
            },
            "location": {
                "latitude": 38.9822,
                "longitude": -94.6708,
                "accuracy": "High",
                "distance": 0.5,
            },
            "vintage": {
                "lastModified": "2023-01-01",
                "pubDate": "2023-01-02",
            },
        },
        {
            "identifier": {"attomId": "124", "fips": "457", "apn": "790"},
            "address": {
                "line1": "456 Elm St",
                "line2": "",
                "locality": "Leawood",
                "countrySubd": "KS",
                "postal1": "66209",
                "postal2": "",
                "postal3": "",
                "country": "US",
                "matchCode": "Exact",
            },
            "location": {
                "latitude": 38.9000,
                "longitude": -94.6500,
                "accuracy": "High",
                "distance": 0.6,
            },
            "vintage": {
                "lastModified": "2023-01-05",
                "pubDate": "2023-01-06",
            },
        },
    ]


@patch("db.get_connection")
def test_insert_property(mock_get_connection, sample_properties):
    """Test insert_property inserts data into a database successfully"""

    #Mock the atabase connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    #Call the function
    insert_property(sample_properties)

    #verify the cursor execute method was called for each property
    assert mock_cursor.execute.call_count == len(sample_properties)

    #verify commit was called
    mock_conn.commit.assert_called_once()

    #ensure cursor and connection are closed
    mock_cursor.close_assert_called_once()
    mock_conn.close.assert_called_once()


