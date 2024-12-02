from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.app.core.mongodb import get_mongodb
from backend.app.services.odds_service import fetch_odds_data, store_match_data, get_all_matches

router = APIRouter()

@router.post("/fetch-odds")
async def fetch_and_store_odds(db: AsyncIOMotorDatabase = Depends(get_mongodb)):
    """Fetch odds from API and store in MongoDB"""
    matches = await fetch_odds_data()
    if not matches:
        raise HTTPException(status_code=400, detail="Failed to fetch odds data")
    
    for match in matches:
        await store_match_data(db, match)
    
    return {"message": "Data inserted successfully"}

@router.get("/matches")
async def get_matches(db: AsyncIOMotorDatabase = Depends(get_mongodb)):
    """Get all matches from database"""
    matches = await get_all_matches(db)
    return matches