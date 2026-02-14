import os

from app.api_clients.odds_api_client import OddsAPIClient
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ODDS_API_KEY")

print(f"API Key loaded: {api_key[:10]}..." if api_key else "No API key found")

if not api_key:
    print("ERROR: ODDS_API_KEY not found in .env file")
    exit

client = OddsAPIClient(api_key=api_key)

print("Fetching NBA games...")
print("Making request to API...")

try:
    games = client.get_games("basketball_nba")
    print(f"Request completed!")
    print(f"Type of response: {type(games)}")
    print(f"Success! Found {len(games)} games")
    
    if games:
        print("\nFirst game:")
        print(f"ID: {games[0]['id']}")
        print(f"Home: {games[0]['home_team']}")
        print(f"Away: {games[0]['away_team']}")
        print(f"Start: {games[0]['commence_time']}")
        print(f"Bookmakers: {len(games[0]['bookmakers'])}")
    else:
        print("No games found in response")
        
except Exception as e:
    print(f"EXCEPTION CAUGHT!")
    print(f"Error type: {type(e)}")
    print(f"Error message: {e}")