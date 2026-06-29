import { Button } from "@/components/ui/button"

const GameCard = ({ game, onBetClick }) => {

    const formatOdds = (odds) => odds > 0 ? `+${odds}` : odds

    return (
        <div className="border rounded-lg p-4 hover:shadow-md hover:border-primary/30 transition-all">
            <div className="flex items-center justify-between mb-3">
                <p className="font-bold">{game.away_team} @ {game.home_team}</p>
                <span className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded">
                    {game.sport}
                </span>
            </div>
            <p className="text-sm text-muted-foreground mb-4">
                {new Date(game.game_date).toLocaleString()}
            </p>
            <div className="flex gap-3">
                <Button onClick={() => onBetClick(game, "away")} variant="outline" className="flex-1 justify-between">
                    <span className="font-bold">{game.away_team}</span>
                    <span className="font-mono font-bold">{formatOdds(game.away_team_odds)}</span>
                </Button>
                <Button onClick={() => onBetClick(game, "home")} variant="outline" className="flex-1 justify-between">
                    <span className="font-bold">{game.home_team}</span>
                    <span className="font-mono font-bold">{formatOdds(game.home_team_odds)}</span>
                </Button>
            </div>
        </div>
    )
}

export default GameCard