from datetime import datetime, timedelta, timezone

from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

games_data = [
    # NBA Games
    {
        "home_team": "Los Angeles Lakers",
        "away_team": "Golden State Warriors",
        "home_team_odds": 1.85,
        "away_team_odds": 2.10,
        "sport": "NBA",
        "game_date": datetime.now() + timedelta(days=1),
        "status": "upcoming"
    },
    {
        "home_team": "Boston Celtics",
        "away_team": "Miami Heat",
        "home_team_odds": 1.70,
        "away_team_odds": 2.25,
        "sport": "NBA",
        "game_date": datetime.now() + timedelta(days=1),
        "status": "upcoming"
    },
    {
        "home_team": "Milwaukee Bucks",
        "away_team": "Denver Nuggets",
        "home_team_odds": 1.95,
        "away_team_odds": 1.95,
        "sport": "NBA",
        "game_date": datetime.now() + timedelta(days=2),
        "status": "upcoming"
    },
    {
        "home_team": "Phoenix Suns",
        "away_team": "Dallas Mavericks",
        "home_team_odds": 2.05,
        "away_team_odds": 1.85,
        "sport": "NBA",
        "game_date": datetime.now() + timedelta(days=2),
        "status": "upcoming"
    },
    {
        "home_team": "Brooklyn Nets",
        "away_team": "Philadelphia 76ers",
        "home_team_odds": 2.20,
        "away_team_odds": 1.75,
        "sport": "NBA",
        "game_date": datetime.now() + timedelta(days=3),
        "status": "upcoming"
    },
    
    # NFL Games
    {
        "home_team": "Kansas City Chiefs",
        "away_team": "Buffalo Bills",
        "home_team_odds": 1.75,
        "away_team_odds": 2.20,
        "sport": "NFL",
        "game_date": datetime.now() + timedelta(days=3),
        "status": "upcoming"
    },
    {
        "home_team": "Dallas Cowboys",
        "away_team": "San Francisco 49ers",
        "home_team_odds": 2.00,
        "away_team_odds": 1.90,
        "sport": "NFL",
        "game_date": datetime.now() + timedelta(days=4),
        "status": "upcoming"
    },
    {
        "home_team": "Philadelphia Eagles",
        "away_team": "Green Bay Packers",
        "home_team_odds": 1.65,
        "away_team_odds": 2.30,
        "sport": "NFL",
        "game_date": datetime.now() + timedelta(days=4),
        "status": "upcoming"
    },
    {
        "home_team": "Miami Dolphins",
        "away_team": "Baltimore Ravens",
        "home_team_odds": 2.15,
        "away_team_odds": 1.80,
        "sport": "NFL",
        "game_date": datetime.now() + timedelta(days=5),
        "status": "upcoming"
    },
    {
        "home_team": "Seattle Seahawks",
        "away_team": "Los Angeles Rams",
        "home_team_odds": 1.95,
        "away_team_odds": 1.95,
        "sport": "NFL",
        "game_date": datetime.now() + timedelta(days=5),
        "status": "upcoming"
    },
    
    # MLB Games
    {
        "home_team": "New York Yankees",
        "away_team": "Boston Red Sox",
        "home_team_odds": 1.80,
        "away_team_odds": 2.15,
        "sport": "MLB",
        "game_date": datetime.now() + timedelta(days=1),
        "status": "upcoming"
    },
    {
        "home_team": "Los Angeles Dodgers",
        "away_team": "San Francisco Giants",
        "home_team_odds": 1.70,
        "away_team_odds": 2.25,
        "sport": "MLB",
        "game_date": datetime.now() + timedelta(days=2),
        "status": "upcoming"
    },
    {
        "home_team": "Houston Astros",
        "away_team": "Texas Rangers",
        "home_team_odds": 1.85,
        "away_team_odds": 2.05,
        "sport": "MLB",
        "game_date": datetime.now() + timedelta(days=2),
        "status": "upcoming"
    },
    {
        "home_team": "Atlanta Braves",
        "away_team": "Philadelphia Phillies",
        "home_team_odds": 1.90,
        "away_team_odds": 2.00,
        "sport": "MLB",
        "game_date": datetime.now() + timedelta(days=3),
        "status": "upcoming"
    },
    {
        "home_team": "Chicago Cubs",
        "away_team": "St. Louis Cardinals",
        "home_team_odds": 2.10,
        "away_team_odds": 1.82,
        "sport": "MLB",
        "game_date": datetime.now() + timedelta(days=4),
        "status": "upcoming"
    },
    
    # NHL Games
    {
        "home_team": "Toronto Maple Leafs",
        "away_team": "Boston Bruins",
        "home_team_odds": 2.10,
        "away_team_odds": 1.82,
        "sport": "NHL",
        "game_date": datetime.now() + timedelta(days=1),
        "status": "upcoming"
    },
    {
        "home_team": "Edmonton Oilers",
        "away_team": "Colorado Avalanche",
        "home_team_odds": 1.95,
        "away_team_odds": 1.95,
        "sport": "NHL",
        "game_date": datetime.now() + timedelta(days=2),
        "status": "upcoming"
    },
    {
        "home_team": "Tampa Bay Lightning",
        "away_team": "Florida Panthers",
        "home_team_odds": 1.88,
        "away_team_odds": 2.03,
        "sport": "NHL",
        "game_date": datetime.now() + timedelta(days=3),
        "status": "upcoming"
    },
    {
        "home_team": "Vegas Golden Knights",
        "away_team": "Dallas Stars",
        "home_team_odds": 1.75,
        "away_team_odds": 2.18,
        "sport": "NHL",
        "game_date": datetime.now() + timedelta(days=4),
        "status": "upcoming"
    },
    {
        "home_team": "New York Rangers",
        "away_team": "New Jersey Devils",
        "home_team_odds": 1.93,
        "away_team_odds": 1.98,
        "sport": "NHL",
        "game_date": datetime.now() + timedelta(days=5),
        "status": "upcoming"
    },
    
    # Soccer Games
    {
        "home_team": "Manchester United",
        "away_team": "Liverpool",
        "home_team_odds": 2.20,
        "away_team_odds": 1.78,
        "sport": "Soccer",
        "game_date": datetime.now() + timedelta(days=2),
        "status": "upcoming"
    },
    {
        "home_team": "Real Madrid",
        "away_team": "Barcelona",
        "home_team_odds": 1.90,
        "away_team_odds": 2.05,
        "sport": "Soccer",
        "game_date": datetime.now() + timedelta(days=3),
        "status": "upcoming"
    },
    {
        "home_team": "Bayern Munich",
        "away_team": "Borussia Dortmund",
        "home_team_odds": 1.65,
        "away_team_odds": 2.35,
        "sport": "Soccer",
        "game_date": datetime.now() + timedelta(days=4),
        "status": "upcoming"
    },
    {
        "home_team": "Paris Saint-Germain",
        "away_team": "Marseille",
        "home_team_odds": 1.55,
        "away_team_odds": 2.55,
        "sport": "Soccer",
        "game_date": datetime.now() + timedelta(days=5),
        "status": "upcoming"
    },
    {
        "home_team": "Arsenal",
        "away_team": "Chelsea",
        "home_team_odds": 1.85,
        "away_team_odds": 2.08,
        "sport": "Soccer",
        "game_date": datetime.now() + timedelta(days=6),
        "status": "upcoming"
    }
]

db = SessionLocal()

try:
    for game_data in games_data:
        game_schema = schemas.GameCreate(**game_data)
        game = crud.create_game(db, game_schema)
        
        print(f"Created: {game_data['home_team']} vs {game_data['away_team']}")
except Exception as e:
    print(f"Error: {e}")

finally:
    db.close()
    print("Database connection closed")
