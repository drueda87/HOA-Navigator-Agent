import psycopg2
from config import DB_CONFIG

def get_connection():
    """Connect to PosgreSQL"""
    # Creates and returns a connection to the PostgreSQL database using credentials from DB_CONFIG.
    return psycopg2.connect(**DB_CONFIG)

def get_zipcodes():
    """retrieve Zip Codes from DB"""
    # try is a keyword used for error handling to prevent crashing, in the event of an error.
    try:
        conn = get_connection()
        # creates a cursuor in the connection to run a query
        cur = conn.cursor()
        cur.execute("Select zip_code FROM zip_codes;")
        # line comprehension that reurns tuples and only grabs first column of zips
        zipcodes = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return zipcodes
    # setting exception to variable e and then concatenating error with text "Database error"
    except Exception as e:
        print(f"Database Error:{e}")
        return []
    
def insert_property(data):
    """Insert property data into database, replacing empty values with 'null'"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        for property in data:
            identifier = property.get("identifier", {})
            address = property.get("address", {})
            location = property.get("location", {})
            vintage = property.get("vintage", {})

            # Replace empty or missing values with "null"
            attom_id = identifier.get("attomId", "null")
            fips = identifier.get("fips", "null")
            apn = identifier.get("apn", "null")
            address_line1 = address.get("line1", "null")
            address_line2 = address.get("line2", "null")
            city = address.get("locality", "null")
            state = address.get("countrySubd", "null")
            zip_code = address.get("postal1", "null")
            postal2 = address.get("postal2", "null")
            postal3 = address.get("postal3", "null")
            country = address.get("country", "null")
            latitude = location.get("latitude", "null")
            longitude = location.get("longitude", "null")
            accuracy = location.get("accuracy", "null")
            distance = location.get("distance", "null")
            match_code = address.get("matchCode", "null")
            last_modified = vintage.get("lastModified", "null")
            pub_date = vintage.get("pubDate", "null")

            try:
                cur.execute("""
                    INSERT INTO properties (
                        attom_id, fips, apn,
                        address_line1, address_line2, city, state, zip_code, postal2, postal3, country,
                        latitude, longitude, accuracy, distance,
                        match_code, last_modified, pub_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (attom_id) DO NOTHING;
                """, (
                    attom_id,
                    fips,
                    apn,
                    address_line1,
                    address_line2,
                    city,
                    state,
                    zip_code,
                    postal2,
                    postal3,
                    country,
                    latitude,
                    longitude,
                    accuracy,
                    distance,
                    match_code,
                    last_modified,
                    pub_date
                ))
            except Exception as row_error:
                print(f"Failed to insert property: {property}, Error: {row_error}")

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database Insert Error: {e}")


def update_property_count(zip_code, property_count):
    """Update the property count in the database for a given ZIP code and state."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
             """
             UPDATE zip_codes
             SET property_count = %s
             WHERE zip_code = %s;
             """,
            (property_count, zip_code)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database Update Error for property_counts: {e}")