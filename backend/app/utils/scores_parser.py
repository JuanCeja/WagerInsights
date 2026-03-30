def parse_winner_from_scores(scores_data: dict) -> str:
    """
    Parse scores data to determine winner.
    
    Returns: "home" or "away"
    Raises: ValueError if game not completed or can't determine winner
    """
    
    #Check if game is completed
    if not scores_data.get("completed"):
        raise ValueError("Game not completed yet")
    
    home_team = scores_data.get("home_team")
    away_team = scores_data.get("away_team")
    scores = scores_data.get("scores", [])
    
    if not scores:
        raise ValueError("No scores available")
    
    #Extract scores (need to match by team name)
    home_score = None
    away_score = None
    
    for score_entry in scores:
        if score_entry["name"] == home_team:
            home_score = int(score_entry["score"])
            
        if score_entry["name"] == away_team:
            away_score = int(score_entry["score"])
            
    if home_score == None or away_score == None:
        raise ValueError("Could not find scores for both teams")
    
    #Determine winner
    if home_score > away_score:
        return "home"
    elif away_score > home_score:
        return "away"
    else:
        raise ValueError("Game ended in a tie. Cannot determine winner")