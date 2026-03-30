import json
import os

from app.api_clients.odds_api_client import OddsAPIClient
from dotenv import load_dotenv

load_dotenv()

client = OddsAPIClient(api_key=os.getenv("ODDS_API_KEY"))

# Test with NBA (likely to have completed games)
print("Fetching NBA scores...")
scores = client.get_scores("basketball_nba")

print(f"\nFound {len(scores)} games with scores\n")

# Print first game to see structure
if scores:
    print("Example game structure:")
    print(json.dumps(scores[0], indent=2))