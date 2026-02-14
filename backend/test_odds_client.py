import os

from app.api_clients.odds_api_client import OddsAPIClient
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ODDS_API_KEY")

import os

from app.api_clients.odds_api_client import OddsAPIClient
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ODDS_API_KEY")

if not api_key:
    print("ERROR: ODDS_API_KEY not found in .env file")
    exit

client = OddsAPIClient(api_key=api_key)

print("Fetching NBA games...")

try:
    games = client.get_games("basketball_nba")
    
    if games:
        print("\nFirst game:")
        print(f"ID: {games[0]['id']}")
        print(f"Home: {games[0]['home_team']}")
        print(f"Away: {games[0]['away_team']}")
        print(f"Start: {games[0]['commence_time']}")
        print(f"Bookmakers: {len(games[0]['bookmakers'])}")
        
except Exception as e:
    print(f"Error: {e}")

if not api_key:
    print("ERROR: ODDS_API_KEY not found in .env file")
    exit

client = OddsAPIClient(api_key=api_key)

print("Fetching NBA games...")

try:
    games = client.get_games("basketball_nba")
    
    if games:
        print("\nFirst game:")
        print(f"ID: {games[0]['id']}")
        print(f"Home: {games[0]['home_team']}")
        print(f"Away: {games[0]['away_team']}")
        print(f"Start: {games[0]['commence_time']}")
        print(f"Bookmakers: {len(games[0]['bookmakers'])}")
        
except Exception as e:
    print(f"Error: {e}")