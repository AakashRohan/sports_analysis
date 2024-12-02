from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MatchBase(BaseModel):
    id: str
    sport_key: str
    sport_title: str
    commence_time: datetime
    home_team: str
    away_team: str

class OddsBase(BaseModel):
    match_id: str
    bookmaker_key: str
    bookmaker_title: str
    last_update: datetime
    market_key: str
    team_name: str
    price: float 