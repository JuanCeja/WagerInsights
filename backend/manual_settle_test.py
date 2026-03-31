import json
import os

from app import crud, models
from app.api_clients.odds_api_client import OddsAPIClient
from app.database import get_db
from app.utils.scores_parser import parse_winner_from_scores
from dotenv import load_dotenv

load_dotenv()

db = next(get_db())

# 1. Get the game from database
game = db.query(models.Game).filter(models.Game.id == 132).first()

print("=== BEFORE SETTLEMENT ===")
print(f"Game ID: {game.id}")
print(f"Teams: {game.away_team} @ {game.home_team}")
print(f"Status: {game.status}")
print(f"Winner: {game.winner}")

# 2. Get scores from API
client = OddsAPIClient(api_key=os.getenv("ODDS_API_KEY"))
scores = client.get_scores("basketball_nba")

print("this how scores looks like: =====================")
print(json.dumps(scores, indent=2))

# Find the matching game in scores
api_game = None
for score_data in scores:
    if score_data["id"] == game.external_api_id:
        api_game = score_data
        break

if not api_game:
    print("ERROR: Game not found in API scores")
    exit()

print(f"\n=== API SCORES ===")
print(f"Home: {api_game['scores'][0]['name']} - {api_game['scores'][0]['score']}")
print(f"Away: {api_game['scores'][1]['name']} - {api_game['scores'][1]['score']}")

# 3. Determine winner
print("this is our api_game data:", api_game)
winner = parse_winner_from_scores(api_game)
print(f"\nWinner: {winner}")

# 4. Settle the game
print("\n=== SETTLING GAME ===")
settled_game = crud.settle_game(db, game.id, winner)
print(f"✓ Game settled!")

# 5. Settle bets
bets_settled = crud.settle_bets_for_game(db, game.id, winner)
print(f"✓ Settled {len(bets_settled)} bets")

# 6. Check final state
db.refresh(game)
print("\n=== AFTER SETTLEMENT ===")
print(f"Status: {game.status}")
print(f"Winner: {game.winner}")
print(f"Settled at: {game.settled_at}")

db.close()