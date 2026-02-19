from datetime import datetime


def parse_api_game_to_model(api_game: dict) -> dict:
    external_api_id = api_game.get("id", None)
    sport = api_game.get("sport_title", None)
    home_team = api_game.get("home_team", None)
    away_team = api_game.get("away_team", None)
    status = "upcoming"
    
    time_str = api_game.get("commence_time", None)
    game_date = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    
    home_team_odds = None
    away_team_odds = None
    
    bookmakers = api_game.get("bookmakers", [])
    
    if bookmakers:
        first_bookmaker = bookmakers[0]
        markets = first_bookmaker.get("markets", [])
        
        h2h_market = None
        for market in markets:
            if market.get("key") == "h2h":
                h2h_market = market
                break
            
        if h2h_market:
            outcomes = h2h_market.get("outcomes", [])
    
            for outcome in outcomes:
                if outcome["name"] == home_team:
                    home_team_odds = outcome["price"]
                if outcome["name"] == away_team:
                    away_team_odds = outcome["price"]
        
    return {
        "external_api_id": external_api_id,
        "sport": sport,
        "home_team": home_team,
        "away_team": away_team,
        "home_team_odds": home_team_odds,
        "away_team_odds": away_team_odds,
        "game_date": game_date,
        "status": status
    }