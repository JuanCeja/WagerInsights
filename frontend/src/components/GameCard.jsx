import { Button } from "@/components/ui/button"

const GameCard = ({ game, onBetClick }) => {

    const formatOdds = (odds) => odds > 0 ? `+${odds}` : odds

    return (
        <div className="border rounded-lg p-4 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
                <p className="font-semibold">{game.away_team} @ {game.home_team}</p>
                <span className="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded">
                    {game.sport}
                </span>
            </div>
            <p className="text-sm text-gray-500 mb-4">
                {new Date(game.game_date).toLocaleString()}
            </p>
            <div className="flex gap-3">
                <Button onClick={() => onBetClick(game, "away")} variant="outline" className="flex-1 justify-between">
                    <span>{game.away_team}</span>
                    <span className="font-semibold">{formatOdds(game.away_team_odds)}</span>
                </Button>
                <Button onClick={() => onBetClick(game, "home")} variant="outline" className="flex-1 justify-between">
                    <span>{game.home_team}</span>
                    <span className="font-semibold">{formatOdds(game.home_team_odds)}</span>
                </Button>
            </div>
        </div>
    )
}

export default GameCard