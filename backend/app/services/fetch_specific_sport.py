import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_odds_for_specific_sport(sport_key):
    """Fetch odds for a specific sport"""
    API_KEY = os.getenv('ODDS_API_KEY')
    ODDS_API_URL = f'https://api.the-odds-api.com/v4/sports/{sport_key}/odds/'
    
    params = {
        'apiKey': API_KEY,
        'regions': 'us',
        'markets': 'h2h'
    }
    
    try:
        response = requests.get(ODDS_API_URL, params=params, timeout=10)
        
        # Save raw response for analysis
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'data/raw_{sport_key}_{timestamp}.json'
        
        os.makedirs('data', exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(response.json(), f, indent=4)
            
        logging.info(f"Data saved to {filename}")
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching odds for {sport_key}: {str(e)}")
        return None

if __name__ == "__main__":
    sport = input("Enter sport key (e.g., 'soccer_epl', 'cricket_test_match'): ")
    data = fetch_odds_for_specific_sport(sport)
    
    if data:
        print(f"\nFetched odds for {sport}")
        print(f"Number of matches: {len(data)}")
    else:
        print("Failed to fetch data") 