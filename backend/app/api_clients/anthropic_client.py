from datetime import datetime

from anthropic import Anthropic

client = Anthropic()

def bet_analyzer(sport: str, home_team: str, away_team: str, bet_type: str, home_team_odds: int | float, away_team_odds: int | float, bet_amount: float, game_date: datetime):

    prompt = f"""You are an expert sports betting analyst. Analyze the following bet and provide a detailed assessment.

    **Bet Details:**
    - Sport: {sport}
    - Matchup: {home_team} (Home) vs {away_team} (Away)
    - Bet Type: {bet_type}
    - Home Team Odds: {home_team_odds}
    - Away Team Odds: {away_team_odds}
    - Bet Amount: ${bet_amount}
    - Game Date: {game_date}

    **Your Analysis Should Cover:**

    1. **Bet Rating** — Rate this bet from 1-10 and explain why.

    2. **Odds Assessment** — Compare the odds ({home_team} at {home_team_odds} vs {away_team} at {away_team_odds}). Who does the market favor and is that pricing accurate? What is the implied probability for each side?

    3. **Home Field Advantage** — How significant is home field advantage for {home_team} in {sport}? Does it meaningfully impact this matchup?

    4. **Injury Updates** — Search for any recent injuries or lineup changes for both {home_team} and {away_team} heading into {game_date}. How do they affect this bet?

    5. **Team Form** — How have both teams been performing recently? Any trends worth noting?

    6. **Recommendation** — Should the bettor proceed with this bet, reduce the amount, or avoid it entirely? Be direct.

    Keep your response concise, data-driven, and honest. Do not sugarcoat a bad bet."""

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": prompt
                }
            ]
    )

    return message.content[0].text