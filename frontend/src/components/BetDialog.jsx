import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { placeBet } from "@/services/betsService"
import { calculatePayout } from "@/utils/betCalculator.js"
import { useState } from "react"
import { toast } from "sonner"

const BetDialog = ({ selectedGame, selectedBetType, onClose, onBetPlaced }) => {
    const [betAmount, setBetAmount] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")

    const odds = selectedBetType === "home" ? selectedGame?.home_team_odds : selectedGame?.away_team_odds
    const teamBetOn = selectedBetType === "home" ? selectedGame?.home_team : selectedGame?.away_team

    const handleSubmit = async () => {
        try {
            setErrorMessage("")
            setIsLoading(true)
            await placeBet({ gameId: selectedGame.id, betType: selectedBetType, betAmount: parseFloat(betAmount) })
            toast.success(`Bet placed! $${betAmount} on ${teamBetOn}`)
            onBetPlaced()
            onClose()
        } catch (error) {
            setErrorMessage(error.response?.data?.detail || "Failed to place bet")
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

                <Button onClick={handleSubmit} disabled={isLoading}>
                    {isLoading ? "Placing bet..." : "Place Bet"}
                </Button>
                {errorMessage && <p className="text-red-500">{errorMessage}</p>}
            </DialogContent>
        </Dialog>
    )
}

export default BetDialog