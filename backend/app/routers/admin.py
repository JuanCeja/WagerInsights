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

@router.post("/sync_games/{sport}", status_code=status.HTTP_200_OK)
def sync_games_from_api(sport: str, db: Session = Depends(get_db)):
    result = _sync_single_sport(sport, db)
    
    if not result.get("success", True):
        raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
    
    return result

@router.get("/available_sports", status_code=status.HTTP_200_OK)
def available_sports():
    client = OddsAPIClient(api_key)
    try:
        list_of_available_sports = client.get_sports()
        return list_of_available_sports
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sports: {str(e)}")

@router.post("/bulk_sync_games", status_code=status.HTTP_200_OK)
def bulk_sync_games(request: schemas.BulkSyncRequest, db: Session = Depends(get_db)):
    results = []
    
    
    for sport in request.sports:
        result = _sync_single_sport(sport, db)
        results.append(result)
    
    successful = sum(1 for r in results if r.get("success"))
    failed = len(results) - successful
    
    return {
        "results": results,
        "total_sports": len(results),
        "successful": successful,
        "failed": failed
    }
    
@router.post("/sync_games/{sport}", status_code=status.HTTP_200_OK)
def sync_games_from_api(sport: str, db: Session = Depends(get_db)):
    result = _sync_single_sport(sport, db)
    
    if not result.get("success", True):
        raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
    
    return result

@router.post("/auto_settle_games/{sport}", status_code=status.HTTP_200_OK)
def automatically_settle_games_in_db(sport: str, db: Session = Depends(get_db)):
    return crud.auto_settle_completed_games(db, sport, api_key)


def _sync_single_sport(sport: str, db: Session) -> dict:
    if not api_key:
        return {
            "sport": sport,
            "success": False,
            "error": "ODDS_API_KEY not configured"
        }
    
    created_games = 0
    updated_games = 0
    
    client = OddsAPIClient(api_key=api_key)
    try:
        games = client.get_games(sport)
    except Exception as e:
        return {
            "sport": sport,
            "success": False,
            "error": f"Failed to fetch from API: {str(e)}"
        }
    
    for game in games:
        parsed_game = parse_api_game_to_model(game)
        
        if parsed_game["home_team_odds"] is None or parsed_game["away_team_odds"] is None:
            continue
    
        existing_game = db.query(models.Game).filter(models.Game.external_api_id == parsed_game["external_api_id"]).first()
        
        crud.sync_game_from_api(db, parsed_game)
        
        if existing_game:
            updated_games += 1
        else:
            created_games += 1
            
    summary = f"{created_games} games were created and {updated_games} were updated"
    
    return {
        "sport": sport,
        "success": True, 
        "total_fetched": len(games),
        "created": created_games,
        "updated": updated_games,
        "summary": summary
    }

