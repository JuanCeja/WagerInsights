import BetDialog from "@/components/BetDialog"
import FeatureCarousel from "@/components/FeatureCarousel"
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

    const scrollToGames = () => {
        document.getElementById("games-section")?.scrollIntoView({ behavior: "smooth" })
    }

    return (
        <>
            <Navbar />

            {/* Hero */}
            <section
                className="border-b py-16"
                style={{ background: "radial-gradient(ellipse 70% 90% at -5% -20%, oklch(0.55 0.22 295 / 0.08) 0%, transparent 65%)" }}
            >
                <div className="max-w-6xl mx-auto px-6">
                    <div className="flex flex-col md:flex-row md:items-center gap-10 md:gap-16">
                        {/* Left: existing hero content — unchanged */}
                        <div className="flex-1">
                            <h2
                                className="text-5xl md:text-6xl font-bold tracking-tight mb-4 leading-tight"
                                style={{ fontFamily: "'Space Grotesk', sans-serif" }}
                            >
                                Smarter bets,<br />backed by data.
                            </h2>
                            <p className="text-lg text-muted-foreground leading-relaxed max-w-xl mb-8">
                                Our AI Bet Analyzer searches the web in real time to evaluate every pick. Make confident decisions, not guesses.
                            </p>
                            <button
                                onClick={scrollToGames}
                                className="inline-flex items-center gap-2 bg-primary text-primary-foreground hover:bg-primary/90 transition-colors px-5 py-2.5 rounded-md text-sm font-medium"
                            >
                                Try the analyzer →
                            </button>
                        </div>

                        {/* Right: feature carousel */}
                        <div className="flex-1">
                            <FeatureCarousel />
                        </div>
                    </div>
                </div>
            </section>

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
                <div id="games-section" className="flex flex-col gap-4">
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