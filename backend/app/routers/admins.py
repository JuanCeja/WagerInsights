from datetime import datetime

from app import auth, crud, models, schemas
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

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