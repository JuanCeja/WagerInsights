import os

from app import crud
from app.database import get_db
from dotenv import load_dotenv

load_dotenv()

db = next(get_db())

print("=== TESTING AUTO-SETTLEMENT ===\n")

# Run auto-settlement for NBA
result = crud.auto_settle_completed_games(
    db=db,
    sport="icehockey_nhl",
    api_key=os.getenv("ODDS_API_KEY")
)

print(f"Sport: {result['sport']}")
print(f"Success: {result['success']}")
print(f"Games settled: {result['games_settled']}")
print(f"Settled game IDs: {result.get('settled_games', [])}")
print(f"Errors: {result.get('errors', 'None')}")

db.close()