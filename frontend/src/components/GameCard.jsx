import { Button } from "@/components/ui/button"

const GameCard = ({ game, onBetClick }) => {

    const formatOdds = (odds) => odds > 0 ? `+${odds}` : odds

    const gameDate = new Date(game.game_date)
    const shortDate = gameDate.toLocaleString(undefined, { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" })
    const longDate = gameDate.toLocaleString()

    return (
        <div className="border rounded-lg p-4 hover:shadow-md hover:border-primary/30 hover:-translate-y-1 transition-all">
            <div className="flex items-center justify-between mb-3">
                <p className="font-bold">{game.away_team} @ {game.home_team}</p>
                <span className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded">
                    {game.sport}
                </span>
            </div>
            <p className="text-sm text-muted-foreground mb-4">
                <span className="sm:hidden">{shortDate}</span>
                <span className="hidden sm:inline">{longDate}</span>
            </p>
            <div className="flex flex-col sm:flex-row gap-3">
                <Button onClick={() => onBetClick(game, "away")} variant="outline" className="flex-1 justify-between min-h-11">
                    <span className="font-bold">{game.away_team}</span>
                    <span className="font-mono font-bold">{formatOdds(game.away_team_odds)}</span>
                </Button>
                <Button onClick={() => onBetClick(game, "home")} variant="outline" className="flex-1 justify-between min-h-11">
                    <span className="font-bold">{game.home_team}</span>
                    <span className="font-mono font-bold">{formatOdds(game.home_team_odds)}</span>
                </Button>
            </div>
        </div>
    )
}

export default GameCard