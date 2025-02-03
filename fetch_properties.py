import time
from db import get_zipcodes
from process import process_zipcode

def main():
    zipcodes = get_zipcodes()

    for zip_code in zipcodes:
        process_zipcode(zip_code)
        time.sleep(1)#avoid rate limiting

if __name__== "__main__":
    main()