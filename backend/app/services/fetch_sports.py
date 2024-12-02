import os
import sys
from app import fetch_all_sports_data
import logging

def main():
    try:
        print("Fetching sports data...")
        data = fetch_all_sports_data()
        
        if data:
            print("\nFetch successful! Data summary:")
            print(f"Number of sports available: {len(data)}")
            print("\nAvailable sports:")
            for sport in data:
                print(f"- {sport.get('title', 'N/A')} ({sport.get('key', 'N/A')})")
        else:
            print("Failed to fetch data. Check api_logs.log for details.")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"Error in fetch_sports.py: {str(e)}")

if __name__ == "__main__":
    main() 