import BetDialog from "@/components/BetDialog"
import GameCard from "@/components/GameCard"
import Navbar from "@/components/Navbar"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useUser } from "@/contexts/UserContext"
import { getGames } from "@/services/gamesService"
import { CalendarX } from "lucide-react"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

function Dashboard() {
    const [games, setGames] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [errorMessage, setErrorMessage] = useState("")
    const [selectedGame, setSelectedGame] = useState(null)
    const [selectedBetType, setSelectedBetType] = useState(null)
    const [selectedSport, setSelectedSport] = useState("all")

    const navigate = useNavigate()

    const { refreshUser, user } = useUser()

    const sports = ["NBA", "NFL", "MLB", "NHL", "NCAAF", "UFL", "EPL", "Liga MX", "UEFA Champions League", "FIFA World Cup"]

    useEffect(() => {
        async function fetchGames() {
            const filters = { status: "upcoming" }
            try {
                if (selectedSport !== "all") {
                    filters.sport = selectedSport
                }
                const data = await getGames(filters)
                setGames(data)
            } catch (error) {
                setErrorMessage("There is an issue retrieving games")
            } finally {
                setIsLoading(false)
            }
        }

        fetchGames()
    }, [selectedSport])


    const handleBetClick = (game, betType) => {
        if (!user) {
            navigate("/login")
            return
        }

        setSelectedGame(game)
        setSelectedBetType(betType)
    }

    const handleCloseDialog = () => {
        setSelectedGame(null)
        setSelectedBetType(null)
    }

    return (
        <>
            <Navbar />

            <div className="max-w-6xl mx-auto px-6 py-8">
                {/* Header row: title on left, sport filter on right */}
                <div className="flex justify-between items-center mb-6">
                    <h1 className="text-3xl font-bold">Dashboard</h1>

                    <Select value={selectedSport} onValueChange={setSelectedSport}>
                        <SelectTrigger className="w-48">
                            <SelectValue placeholder="Filter by sport" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="all">All Sports</SelectItem>
                            {sports.map((sport) => (
                                <SelectItem key={sport} value={sport}>{sport}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>

                <BetDialog
                    key={selectedGame?.id}
                    selectedGame={selectedGame}
                    selectedBetType={selectedBetType}
                    onClose={handleCloseDialog}
                    onBetPlaced={refreshUser}
                />

                {/* Games list */}
                <div className="flex flex-col gap-4">
                    {isLoading ? (
                        <p>Loading games...</p>
                    ) : errorMessage ? (
                        <p className="text-red-500">{errorMessage}</p>
                    ) : games.length === 0 ? (
                        <div className="text-center py-12">
                            <CalendarX className="mx-auto h-12 w-12 text-gray-400" />
                            <h3 className="mt-4 text-lg font-semibold">No upcoming games</h3>
                            <p className="text-gray-500 mt-1">Try selecting a different sport.</p>
                        </div>
                    ) : (
                        games.map((game) => (
                            <GameCard key={game.id} game={game} onBetClick={handleBetClick} />
                        ))
                    )}
                </div>
            </div>
        </>
    )
}

export default Dashboard