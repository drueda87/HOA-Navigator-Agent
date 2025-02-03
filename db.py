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
        # creatores a cursuor in the connection to run a query
        cur = conn.cursor()
        cur.execute("Select zip_code FROM zip_codes;")
        # line comprehension that reurns tuples and only grabs first column of zips
        zipodes = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return zipcodes
    # setting exception to variable e and then concatenating error with text "Database error"
    except Exception as e:
        print(f"Database Error:{e}")
        return []
    
def insert_property(data):
    """insert property data into database"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        for property in data:
            identifier = property.get("identifier",{})
            address = property.get("address",{})
            location = property.ge("location",{})
            vintage = property.get("vintage",{})
            
            # execute(SQL Query, values)
            # value substiution used to prevent direct SQL injection.
            cur.execute("""
                INSERT INTO properties (
                    attom_id, fips, apn, 
                    address_line1, address_line2, city, state, zip_code, postal2, postal3, country,
                    latitude, longitude, accuracy, distance,
                    match_code, last_modified, pub_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (attom_id) DO NOTHING;
            """, (
                identifier.get("attomId"),
                identifier.get("fips"),
                identifier.get("apn"),
                address.get("line1"),
                address.get("line2"),
                address.get("locality"),
                address.get("countrySubd"),
                address.get("postal1"),
                address.get("postal2"),
                address.get("postal3"),
                address.get("country"),
                location.get("latitude"),
                location.get("longitude"),
                location.get("accuracy"),
                location.get("distance"),
                address.get("matchCode"),
                vintage.get("lastModified"),
                vintage.get("pubDate")
            ))   
        # commit() saves changes applied to db.
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database Insert Error: {e}")