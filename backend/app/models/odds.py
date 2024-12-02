from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Outcome(BaseModel):
    name: str
    price: float

class Market(BaseModel):
    key: str
    outcomes: List[Outcome]

class Bookmaker(BaseModel):
    key: str
    title: str
    last_update: datetime
    markets: List[Market]

class Match(BaseModel):
    id: str = Field(alias="_id")
    sport_key: str
    sport_title: str
    commence_time: datetime
    home_team: str
    away_team: str
    bookmakers: List[Bookmaker] 