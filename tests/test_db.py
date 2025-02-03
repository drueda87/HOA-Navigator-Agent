from db import get_zipcodes

def test_get_zipcodes():
    zipcodes = get_zipcodes()
    assert isinstance(zipcodes, list)  # Should return a list
    assert all(isinstance(z, str) for z in zipcodes)  # Ensure all items are strings
