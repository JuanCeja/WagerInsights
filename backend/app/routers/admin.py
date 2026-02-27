import os
from datetime import datetime

from app import auth, crud, models, schemas
from app.api_clients.odds_api_client import OddsAPIClient
from app.database import get_db
from app.utils.odds_parser import parse_api_game_to_model
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

load_dotenv()
api_key = os.getenv("ODDS_API_KEY")

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/games/settle_game/{game_id}", response_model=schemas.SettlementSummary, status_code=status.HTTP_200_OK)
def settle_game_and_bets(game_update: schemas.GameSettleUpdate, game_id:int, db: Session = Depends(get_db)):
    try:
        settled_game = crud.settle_game(db, game_id, game_update.winner)
        bets_settled = crud.settle_bets_for_game(db, game_id, game_update.winner)
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
        
        elif "already been settled" in error_msg.lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflict: Game has already been settled")
        
        elif "must be" in error_msg.lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Winner must be 'home' or 'away'")
        
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)
        
    summary = {
        "settled_game": settled_game,
        "bets_settled": bets_settled
    }
    
    return summary

@router.post("/admin/sync_games/{sport}", list[response_model=schemas.GameResponse], status_code=status.HTTP_200_OK)
def sync_games_from_api(sport: str, db: Session = Depends(get_db)):
    created_games = 0
    updated_games = 0
    
    client = OddsAPIClient(api_key=api_key)
    games = client.get_games(sport)
    
    for game in games:
        parsed_game = parse_api_game_to_model(game)
        current_game = crud.get_game_by_id(db, parsed_game["external_api_id"])
        if current_game:
            current_game = parsed_game
            updated_games += 1
        else:
            crud.create_game(db, parsed_game)
            created_games += 1
    
    print(f"{created_games} games were created and {updated_games} were updated")
    return games