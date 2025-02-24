import psycopg2
import os
from psycopg2.extras import RealDictCursor


DB_CONFIG = {
    "dbname": "real_estate",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "host": "localhost",
    "port": "5432"
    }

def get_db_connection():
    """Establish and return a database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Database Connection Successful")
        return conn
    except Exception as e:
        print(f"error connecting to the database: {e}")
        return None
    
