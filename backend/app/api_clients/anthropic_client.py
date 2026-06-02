from datetime import datetime

from anthropic import Anthropic

client = Anthropic()

def bet_analyzer(sport: str, home_team: str, away_team: str, bet_type: str, home_team_odds: int | float, away_team_odds: int | float, bet_amount: float, game_date: datetime):

    prompt = f"""You are a sports betting analyst evaluating a proposed bet for the user. Your job is to assess the actual value of this bet objectively, using the rubric below. Be honest in both directions — flag genuine value as readily as overpriced markets.

    **Bet Details:**
    - Sport: {sport}
    - Matchup: {home_team} (Home) vs {away_team} (Away)
    - Bet Type: {bet_type}
    - Home Team Odds: {home_team_odds}
    - Away Team Odds: {away_team_odds}
    - Bet Amount: ${bet_amount}
    - Game Date: {game_date}

    **Important context about the rubric:** Sportsbooks price most games close to fair value with a built-in margin (vig), so the average bet a recreational bettor places lands around 4-6 on this scale. This is normal, not a warning — it means the market is doing its job. Reserve scores below 4 for bets where the user is taking the worse side of a clearly mispriced market, and scores above 7 for cases where there's identifiable value beyond the standard market spread.

    **Your Analysis Should Cover:**

    1. **Bet Rating** — Rate this bet from 1-10 using this rubric:
    - 1-2: Clear value trap, the user is on the wrong side
    - 3-4: Below-average value, market favors the other side or odds are inflated
    - 5-6: Fairly priced, standard market bet — no clear edge either direction
    - 7-8: Identifiable value, the odds offer better return than the implied probability suggests
    - 9-10: Significant market mispricing (rare)

    2. **Odds Assessment** — Compare {home_team} at {home_team_odds} vs {away_team} at {away_team_odds}. What is the implied probability for each side? Is the price reasonable, or is one side offering better value than the implied probability suggests?

    3. **Home Field Advantage** — How significant is home field advantage for {home_team} in {sport}? Does it meaningfully impact this matchup?

    4. **Injury & Lineup Context** — Note any historically known patterns about either team's roster. Do not speculate on current injury status you cannot verify; flag that the bettor should confirm current reports before placing.

    5. **Team Form** — How have both teams been performing recently? Any trends worth noting?

    6. **Recommendation** — Choose one: **Strong play (consider increasing)**, **Solid bet (proceed as planned)**, **Standard market bet (proceed if you like the matchup)**, **Marginal (reduce amount)**, or **Pass (avoid)**. Tie this directly to the rating you gave — a 5-6 is a "standard market bet," not a warning.

    Be balanced. A 5/10 is a normal sportsbook-priced bet, not a failure. Reserve "Pass" for bets you genuinely judge as 1-3."""
    
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