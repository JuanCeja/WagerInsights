import requests


class OddsAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_URL = "https://api.the-odds-api.com/v4"
        
    def get_games(self, sport: str):
        try:
            response = requests.get(
                f"{self.base_URL}/sports/{sport}/odds",
                params={
                    "apiKey": self.api_key,
                    "regions": "us",
                    "markets": "h2h",
                    "oddsFormat": "american"
            })
        
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"API returned {response.status_code}: {response.text}")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")