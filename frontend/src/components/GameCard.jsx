import { Button } from "@/components/ui/button"
import { useState } from "react"

const GameCard = ({ game }) => {
    const [gameId, setGameId] = useState(game.gameId)
    const [betType, setBetType] = useState("")
    const [homeOdds, setHomeOdds] = useState(game.home_team_odds)
    const [awayOdds, setAwayOdds] = useState(game.away_team_odds)

    const handleOnBet = (betType, odds) => {
        setBetType(betType)
        console.log({
            gameId: {gameId},
            betType: {betType},
            odds: {odds}
        })
    }

    return (
        <div className="border rounded-lg p-4">
            <p className="font-semibold">{game.away_team} @ {game.home_team}</p>
            <p className="text-sm text-gray-600">{game.sport} • {new Date(game.game_date).toLocaleString()}</p>
            <div className="flex gap-4 mt-2">
                <span>Home: {game.home_team_odds > 0 ? `+${game.home_team_odds}` : game.home_team_odds}</span>
                <span>Away: {game.away_team_odds > 0 ? `+${game.away_team_odds}` : game.away_team_odds}</span>
            </div>
            <div>
                <Button onClick={() => handleOnBet("away", game.away_team_odds)} variant="default">Place bet on {game.away_team} {game.away_team_odds > 0 ? `+${game.away_team_odds}` : game.away_team_odds}</Button>
                <Button onClick={() => handleOnBet("home", game.home_team_odds)} variant="default">Place bet on {game.home_team} {game.home_team_odds > 0 ? `+${game.home_team_odds}` : game.home_team_odds}</Button>
            </div>
        </div>
    )
}

export default GameCard