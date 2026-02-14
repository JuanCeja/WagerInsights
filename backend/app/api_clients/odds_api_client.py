import requests


class OddsAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_URL = "https://api.the-odds-api.com/v4"
        
    def get_games(self, sport: str):
        print(f"[DEBUG] Calling API for sport: {sport}")
        try:
            url = f"{self.base_URL}/sports/{sport}/odds"
            params = {
                "apiKey": self.api_key,
                "regions": "us",
                "markets": "h2h",
                "oddsFormat": "american"
            }
            
            print(f"[DEBUG] URL: {url}")
            print(f"[DEBUG] Params: {params}")
            
            response = requests.get(url, params=params)
            
            print(f"[DEBUG] Status Code: {response.status_code}")
            print(f"[DEBUG] Response headers: {response.headers}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[DEBUG] Got {len(data)} games")
                return data
            else:
                raise Exception(f"API returned {response.status_code}: {response.text}")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")