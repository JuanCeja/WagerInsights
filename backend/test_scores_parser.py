import os

from app.api_clients.odds_api_client import OddsAPIClient
from app.utils.scores_parser import parse_winner_from_scores
from dotenv import load_dotenv

load_dotenv()

client = OddsAPIClient(api_key=os.getenv("ODDS_API_KEY"))

# Get NBA scores
scores = client.get_scores("basketball_nba")

# Test with first completed game
if scores:
    game = scores[0]
    print(f"Game: {game['away_team']} @ {game['home_team']}")
    print(f"Score: {game['scores'][1]['score']} - {game['scores'][0]['score']}")
    print(f"Completed: {game['completed']}")
    
    # Parse winner
    winner = parse_winner_from_scores(game)
    print(f"\nWinner: {winner}")
    
    # Verify it's correct
    if winner == "home":
        print(f"✓ Home team ({game['home_team']}) won!")
    else:
        print(f"✓ Away team ({game['away_team']}) won!")