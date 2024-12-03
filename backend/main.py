from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
import httpx
import hashlib
from fastapi import HTTPException

# Create FastAPI instance
app = FastAPI(title="Sports Analysis API")

# MongoDB connection
MONGODB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.sports_odds
matches_collection = db.matches

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Sports Analysis API"}

@app.get("/api/v1/matches")
async def get_matches():
    try:
        cursor = matches_collection.find({})
        matches = await cursor.to_list(length=None)
        return matches
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/v1/fetch-odds")
async def fetch_and_store_odds():
    API_KEY = "5fe5ad3125788a7f7806ce5b7644fa4b"  # Your API key
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
