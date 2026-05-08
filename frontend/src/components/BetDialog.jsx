import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog"

const BetDialog = ({ selectedGame, selectedBetType, onClose }) => {
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
            </DialogContent>
        </Dialog>
    )
}

export default BetDialog