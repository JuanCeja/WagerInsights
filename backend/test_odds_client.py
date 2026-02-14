import os

from app.api_clients.odds_api_client import OddsAPIClient
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ODDS_API_KEY")

if not api_key:
    exit

client = OddsAPIClient(api_key=api_key)

try:
    sports = client.get_sports()
    
    active_sports = [s for s in sports if s.get("has_outrights") == False]
    
    print(f"\nFound {len(active_sports)} active sports:")
    
    for sport in active_sports[:10]:
        print(f" - {sport['key']}: {sport['title']}")
        
    if active_sports:
        test_sport = active_sports[0]['key']
        print(f"\n=== Testing with {test_sport} ===")
        games = client.get_games(test_sport)
        print(f"Found {len(games)} games")
    
        if games:
            print(f"\nFirst game:")
            print(f"  Home: {games[0]['home_team']}")
            print(f"  Away: {games[0]['away_team']}")
            print(f"  Start: {games[0]['commence_time']}")

except Exception as e:
    print(f"Error message: {e}")