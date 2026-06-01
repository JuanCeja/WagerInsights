import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { analyzeBet, placeBet } from "@/services/betsService"
import { calculatePayout } from "@/utils/betCalculator.js"
import { Loader2, Sparkles } from "lucide-react"
import { useState } from "react"
import { toast } from "sonner"

const BetDialog = ({ selectedGame, selectedBetType, onClose, onBetPlaced }) => {
    const [betAmount, setBetAmount] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")

    const [analysisText, setAnalysisText] = useState("")
    const [analysisError, setAnalysisError] = useState("")
    const [isAnalysisLoading, setIsAnalysisLoading] = useState(false)


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

    const handleAnalyze = async () => {
        try {
            setAnalysisText("")
            setAnalysisError("")
            setIsAnalysisLoading(true)
            const response = await analyzeBet({ gameId: selectedGame.id, betType: selectedBetType, betAmount: parseFloat(betAmount) })
            setAnalysisText(response.analysis)
        } catch (error) {
            setAnalysisError(error.response?.data?.detail || "Failed to fetch bet analysis")
        } finally {
            setIsAnalysisLoading(false)
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

                {/* Analyze button */}
                <Button
                    onClick={handleAnalyze}
                    disabled={isAnalysisLoading || !betAmount}
                    variant="outline"
                >
                    {isAnalysisLoading ? (
                        <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Analyzing...
                        </>
                    ) : (
                        <>
                            <Sparkles className="mr-2 h-4 w-4" />
                            Analyze Bet
                        </>
                    )}
                </Button>

                {/* Analysis output area */}
                {analysisError && (
                    <p className="text-red-500 text-sm">{analysisError}</p>
                )}
                {analysisText && (
                    <div className="max-h-64 overflow-y-auto text-sm whitespace-pre-wrap p-3 rounded-md bg-muted/40 border">
                        {analysisText}
                    </div>
                )}

                {/* Place Bet button */}
                <Button onClick={handleSubmit} disabled={isLoading}>
                    {isLoading ? "Placing bet..." : "Place Bet"}
                </Button>
                {errorMessage && <p className="text-red-500">{errorMessage}</p>}
            </DialogContent>
        </Dialog>
    )
}

export default BetDialog