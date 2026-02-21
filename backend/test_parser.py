import json
import os

from app.api_clients.odds_api_client import OddsAPIClient
from app.utils.odds_parser import parse_api_game_to_model
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ODDS_API_KEY")

if not api_key:
    print("ERROR: ODDS_API_KEY not found in .env file")
    exit()

client = OddsAPIClient(api_key=api_key)

print("=== Testing Parser ===")
try:
    # Fetch games from API
    api_games = client.get_games("americanfootball_ncaaf")
    print(f"Fetched {len(api_games)} games from API\n")
    
    if api_games:
        # Parse the first game
        first_game = api_games[0]
        print("=== RAW API DATA ===")
        print(json.dumps(first_game, indent=2))
        
        print("\n=== PARSED RESULT ===")
        parsed_game = parse_api_game_to_model(first_game)
        print(json.dumps(parsed_game, indent=2, default=str))  # default=str handles datetime
        
        print("\n=== VALIDATION ===")
        print(f"✓ External ID: {parsed_game['external_api_id']}")
        print(f"✓ Sport: {parsed_game['sport']}")
        print(f"✓ Teams: {parsed_game['home_team']} vs {parsed_game['away_team']}")
        print(f"✓ Home odds: {parsed_game['home_team_odds']}")
        print(f"✓ Away odds: {parsed_game['away_team_odds']}")
        print(f"✓ Game date: {parsed_game['game_date']}")
        print(f"✓ Status: {parsed_game['status']}")
        
        # Check that odds match the teams correctly
        print("\n=== ODDS MATCH CHECK ===")
        print(f"Home team ({parsed_game['home_team']}): {parsed_game['home_team_odds']}")
        print(f"Away team ({parsed_game['away_team']}): {parsed_game['away_team_odds']}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()