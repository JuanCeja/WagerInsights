import requests


class OddsAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_URL = "https://api.the-odds-api.com/v4"
        
    def get_games(self, sport: str):
        response = requests.get(f"{self.base_URL}/sports/{sport}/odds?regions=us&markets=us&oddsFormat=american")
        
        try:
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []