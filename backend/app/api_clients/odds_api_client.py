import requests


class OddsAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_URL = "https://api.the-odds-api.com/v4"
        
    def get_games(self, sport: str):
        """Fetch games and odds for a specific sport (e.g., 'basketball_nba')"""
        try:
            url = f"{self.base_URL}/sports/{sport}/odds"
            params = {
                "apiKey": self.api_key,
                "regions": "us",           # US sportsbooks
                "markets": "h2h",          # Head-to-head (moneyline) betting
                "oddsFormat": "american"   # -150, +200 format
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data  # Returns array of game objects
            else:
                raise Exception(f"API returned {response.status_code}: {response.text}")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")
        
    def get_sports(self):
        """Get list of all available sports from The Odds API"""
        try:
            url = f"{self.base_URL}/sports/?apiKey={self.api_key}"
            response = requests.get(url)
            
            if response.status_code == 200:
                sports = response.json()
                return sports  # Returns array of sport objects
            else:
                raise Exception(f"API returned {response.status_code}: {response.text}")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")