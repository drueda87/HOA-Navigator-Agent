from api import fetch_addresses

# Choose a single ZIP code to test
zip_code = "66211"

# Fetch addresses from the API and attempt to write to the DB
print(f"Fetching and inserting properties for ZIP {zip_code}...")
fetch_addresses(zip_code)

print("✅ Data fetching and insertion completed.")
print("➡ Now, manually check your database to confirm records were added.")
