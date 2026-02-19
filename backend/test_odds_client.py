import json
import os

from app.api_clients.odds_api_client import OddsAPIClient
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ODDS_API_KEY")

if not api_key:
    print("ERROR: ODDS_API_KEY not found in .env file")
    exit()

client = OddsAPIClient(api_key=api_key)

print("=== Fetching NCAAF games ===")
try:
    games = client.get_games("americanfootball_ncaaf")
    print(f"Found {len(games)} games\n")
    
    if games:
        # Print the FULL structure of first game
        print("=== FULL FIRST GAME DATA ===")
        print(json.dumps(games[0], indent=2))
        
        print("\n=== KEY OBSERVATIONS ===")
        print(f"External ID: {games[0]['id']}")
        print(f"Sport: {games[0]['sport_title']}")
        print(f"Teams: {games[0]['home_team']} vs {games[0]['away_team']}")
        print(f"Start time: {games[0]['commence_time']}")
        print(f"Number of bookmakers: {len(games[0]['bookmakers'])}")
        
        # Look at first bookmaker's odds
        if games[0]['bookmakers']:
            bookmaker = games[0]['bookmakers'][0]
            print(f"\nFirst bookmaker: {bookmaker['title']}")
            print(f"Markets: {[m['key'] for m in bookmaker['markets']]}")
            
            # Get h2h odds
            h2h_market = next((m for m in bookmaker['markets'] if m['key'] == 'h2h'), None)
            if h2h_market:
                print(f"\nH2H Odds:")
                for outcome in h2h_market['outcomes']:
                    print(f"  {outcome['name']}: {outcome['price']}")
    
except Exception as e:
    print(f"Error: {e}")