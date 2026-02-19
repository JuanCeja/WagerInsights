import requests


class OddsAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_URL = "https://api.the-odds-api.com/v4"
        
    def get_games(self, sport: str):
        try:
            url = f"{self.base_URL}/sports/{sport}/odds"
            params = {
                "apiKey": self.api_key,
                "regions": "us",
                "markets": "h2h",
                "oddsFormat": "american"
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                raise Exception(f"API returned {response.status_code}: {response.text}")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")
        
    def get_sports(self):        
        try:
            url = f"{self.base_URL}/sports/?apiKey={self.api_key}"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                sports = response.json()
                return sports
            else:
                raise Exception(f"API returned {response.status_code}: {response.text}")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")