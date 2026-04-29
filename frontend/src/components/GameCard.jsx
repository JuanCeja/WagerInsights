const GameCard = ({ game }) => {
    return (
        <div className="border rounded-lg p-4">
            <p className="font-semibold">{game.away_team} @ {game.home_team}</p>
            <p className="text-sm text-gray-600">{game.sport} • {new Date(game.game_date).toLocaleString()}</p>
            <div className="flex gap-4 mt-2">
                <span>Home: {game.home_team_odds > 0 ? `+${game.home_team_odds}` : game.home_team_odds}</span>
                <span>Away: {game.away_team_odds > 0 ? `+${game.away_team_odds}` : game.away_team_odds}</span>
            </div>
        </div>
    )
}

export default GameCard