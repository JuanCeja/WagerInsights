import { Button } from "@/components/ui/button"

const GameCard = ({ game, onBetClick }) => {

    const formatOdds = (odds) => odds > 0 ? `+${odds}` : odds

    return (
        <div className="border rounded-lg p-4">
            <p className="font-semibold">{game.away_team} @ {game.home_team}</p>
            <p className="text-sm text-gray-600">{game.sport} • {new Date(game.game_date).toLocaleString()}</p>
            <div className="flex gap-4 mt-4">
                <Button onClick={() => onBetClick(game, "away")} variant="outline" className="flex-1">
                    {game.away_team} {formatOdds(game.away_team_odds)}
                </Button>
                <Button onClick={() => onBetClick(game, "home")} variant="outline" className="flex-1">
                    {game.home_team} {formatOdds(game.home_team_odds)}
                </Button>
            </div>
        </div>
    )
}

export default GameCard