def calculate_payout(bet_amount: float, odds: float) -> float:
    """Calculate total payout (stake + profit) for American odds."""
    if odds > 0:
        # Positive odds: profit = stake * (odds / 100)
        profit = bet_amount * (odds / 100)
    else:
        # Negative odds: profit = stake * (100 / abs(odds))
        profit = bet_amount * (100 / abs(odds))
    
    return bet_amount + profit