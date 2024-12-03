from fastapi import APIRouter, HTTPException
from typing import List
import httpx
import hashlib
import json
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

# MongoDB connection
MONGODB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.sports_odds
matches_collection = db.matches

@router.post("/fetch-odds")
async def fetch_and_store_odds():
    API_KEY = "YOUR_API_KEY"  # Replace with your API key
    SPORT = "cricket_test_match"
    REGIONS = "eu"
    MARKETS = "h2h"
    ODDS_FORMAT = "decimal"

    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"
    params = {
        "api_key": API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
        "oddsFormat": ODDS_FORMAT
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            matches = response.json()

            # Store each match in MongoDB
            for match in matches:
                # Create a unique ID based on teams and time
                match_data = f"{match['home_team']}{match['away_team']}{match['commence_time']}"
                match['_id'] = hashlib.md5(match_data.encode()).hexdigest()
                
                # Upsert the match data
                await matches_collection.update_one(
                    {'_id': match['_id']},
                    {'$set': match},
                    upsert=True
                )

            return {"message": "Data inserted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/matches")
async def get_matches():
    try:
        cursor = matches_collection.find({})
        matches = await cursor.to_list(length=None)
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))