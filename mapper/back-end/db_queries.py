from db_connection import get_db_connection
from psycopg2.extras import RealDictCursor

def get_property_data():
    """Fetch address and coordinate data from the database"""
    conn = get_db_connection()
    if not conn:
        return[]
    
    try:
        with conn.cursor(cursor_factor=RealDictCursor) as cursor:
            query = """
            SELECT id, address_line1, city, state, zip_code, latitude, longitutde, sub_division_id, subdivision, block_num, lot_num
            FROM properties"""
            cursor.execute(query)
            properties = cursor.fetchall()
            return properties
    except Exception as e:
        print(f"Error fetching property data: {e}")
        return []
    finally:
        conn.close()