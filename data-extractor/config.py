import os
# config.py - store database and API credentials

DB_CONFIG = {
    "dbname": "real_estate",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "host": "localhost",
    "port": "5432"

}

API_URL = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/address"
API_KEY = "3de70d6c36bc3044a2db1f6cf6de89e7"

