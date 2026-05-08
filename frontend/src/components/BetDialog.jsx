import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { placeBet } from "@/services/betsService"
import { calculatePayout } from "@/utils/betCalculator.js"
import { useState } from "react"

const BetDialog = ({ selectedGame, selectedBetType, onClose }) => {
    const [betAmount, setBetAmount] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")

    const odds = selectedBetType === "home" ? selectedGame?.home_team_odds : selectedGame?.away_team_odds

    const handleSubmit = () => {
        setIsLoading(true)
        try {
            placeBet({gameId: selectedGame.id, betType: selectedBetType, betAmount: parseFloat(betAmount)})
            onClose()
        } catch(error) {
            setErrorMessage(error) 
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <Dialog open={selectedGame !== null} onOpenChange={onClose}>
            <DialogContent>
                <DialogTitle>Place Your Bet</DialogTitle>
                <DialogDescription>
                    {selectedGame?.away_team} @ {selectedGame?.home_team}
                </DialogDescription>
                <DialogDescription>
                    Bet type: {selectedBetType}
                </DialogDescription>
                <Input
                    type="number"
                    placeholder="Enter bet amount"
                    value={betAmount}
                    onChange={(e) => setBetAmount(e.target.value)}
                />
                <p>Potential Payout: ${calculatePayout(betAmount, odds)}</p>
                {
                    isLoading ? <Button onClick={handleSubmit}>Place Bet</Button>
                    :  <p color="red"> {errorMessage} </p>
                }
            </DialogContent>
        </Dialog>
    )
}

export default BetDialog