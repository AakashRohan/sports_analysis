import os
from datetime import datetime
import requests
from motor.motor_asyncio import AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()

async def fetch_odds_data() -> list:
    """Fetch odds data from the API"""
    API_KEY = os.getenv('ODDS_API_KEY')
    url = f'https://api.the-odds-api.com/v4/sports/cricket_test_match/odds/?apiKey={API_KEY}&regions=eu&markets=h2h'
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

async def store_match_data(db: AsyncIOMotorDatabase, match_data: dict):
    """Store match data in MongoDB"""
    # Use match ID as MongoDB document ID
    match_data['_id'] = match_data.pop('id')
    
    # Convert ISO string to datetime
    match_data['commence_time'] = datetime.fromisoformat(match_data['commence_time'].replace('Z', ''))
    
    # Convert bookmaker last_update times
    for bookmaker in match_data['bookmakers']:
        bookmaker['last_update'] = datetime.fromisoformat(bookmaker['last_update'].replace('Z', ''))
    
    # Upsert the document
    await db.matches.update_one(
        {'_id': match_data['_id']},
        {'$set': match_data},
        upsert=True
    )

async def get_all_matches(db: AsyncIOMotorDatabase):
    """Retrieve all matches from MongoDB"""
    cursor = db.matches.find()
    matches = await cursor.to_list(length=100)
    return matches 