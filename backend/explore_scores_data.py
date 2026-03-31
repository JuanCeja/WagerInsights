import json
import os

from app import models
from app.api_clients.odds_api_client import OddsAPIClient
from app.database import get_db
from dotenv import load_dotenv

load_dotenv()

# 1. What does the API return?
client = OddsAPIClient(api_key=os.getenv("ODDS_API_KEY"))
scores = client.get_scores("basketball_nba")

print("=== API SCORES DATA ===")
print(f"Total games: {len(scores)}")
print(f"\nFirst game structure:")
print(json.dumps(scores[0], indent=2))

# 2. What games are in our database?
db = next(get_db())
our_games = db.query(models.Game).filter(
    models.Game.sport == "NBA"
).all()

print(f"\n=== OUR DATABASE ===")
print(f"Total NBA games in DB: {len(our_games)}")
print(f"\nFirst game in DB:")
print(f"  ID: {our_games[0].id}")
print(f"  External API ID: {our_games[0].external_api_id}")
print(f"  Teams: {our_games[0].away_team} @ {our_games[0].home_team}")
print(f"  Status: {our_games[0].status}")

# 3. Can we match them?
api_game = scores[0]
api_id = api_game['id']

matching_game = db.query(models.Game).filter(
    models.Game.external_api_id == api_id
).first()

print(f"\n=== MATCHING TEST ===")
print(f"API game ID: {api_id}")
if matching_game:
    print(f"✓ Found matching game in DB: {matching_game.id}")
    print(f"  Current status: {matching_game.status}")
    print(f"  Completed in API: {api_game['completed']}")
else:
    print("✗ No matching game found in DB")

db.close()

# 4. How many games can we settle?
print("\n=== SETTLEABLE GAMES ===")

settleable = []
already_settled = []
not_in_db = []

for api_game in scores:
    if not api_game.get("completed"):
        continue
    
    api_id = api_game["id"]
    db_game = db.query(models.Game).filter(
        models.Game.external_api_id == api_id
    ).first()
    
    if not db_game:
        not_in_db.append(api_id)
        continue
    
    if db_game.status == "completed":
        already_settled.append(db_game.id)
    else:
        settleable.append({
            "db_id": db_game.id,
            "api_id": api_id,
            "teams": f"{db_game.away_team} @ {db_game.home_team}",
            "status": db_game.status
        })

print(f"Completed games in API: {len(scores)}")
print(f"Games we CAN settle: {len(settleable)}")
print(f"Already settled: {len(already_settled)}")
print(f"Not in our DB: {len(not_in_db)}")

if settleable:
    print(f"\n✓ Games ready to settle:")
    for game in settleable[:5]:  # Show first 5
        print(f"  - Game {game['db_id']}: {game['teams']} (status: {game['status']})")