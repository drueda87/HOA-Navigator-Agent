import pytest
import re
from unittest.mock import patch, MagicMock
from unittest import mock
from db import get_zipcodes, update_property_count





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


@mock.patch("db.get_connection")  # Mock the database connection
def test_update_property_count(mock_get_connection):
    """Test that update_property_count executes the correct SQL update query"""

    # Create a mock connection and cursor
    mock_conn = mock.Mock()
    mock_cursor = mock.Mock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Call the function
    zip_code = "66208"
    property_count = 2500
    update_property_count(zip_code, property_count)

    # Normalize expected SQL query (remove excess spaces and newlines)
    expected_query = """
        UPDATE zip_codes
        SET property_count = %s
        WHERE zip_code = %s;
    """.strip()
    
    # Get the actual query executed
    actual_query = mock_cursor.execute.call_args[0][0].strip()

    # Normalize whitespace for comparison (collapse multiple spaces into one)
    def normalize_whitespace(sql):
        return re.sub(r"\s+", " ", sql).strip()

    assert normalize_whitespace(actual_query) == normalize_whitespace(expected_query), f"SQL Mismatch:\nExpected:\n{expected_query}\nActual:\n{actual_query}"

    # Ensure the function was called with the correct values
    mock_cursor.execute.assert_called_once_with(mock.ANY, (property_count, zip_code))
