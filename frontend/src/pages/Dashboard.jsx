import BetDialog from "@/components/BetDialog"
import GameCard from "@/components/GameCard"
import Navbar from "@/components/Navbar"
import { useUser } from "@/contexts/UserContext"
import { getGames } from "@/services/gamesService"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

function Dashboard() {
    const [games, setGames] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [errorMessage, setErrorMessage] = useState("")
    const [selectedGame, setSelectedGame] = useState(null)
    const [selectedBetType, setSelectedBetType] = useState(null)

    const navigate = useNavigate()

    const { refreshUser, user } = useUser()

    useEffect(() => {
        async function fetchGames() {
            try {
                const data = await getGames({ status: "upcoming" })
                setGames(data)
            } catch (error) {
                setErrorMessage("There is an issue retrieving games")
            } finally {
                setIsLoading(false)
            }
        }

        fetchGames()
    }, [])


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
            <div className='min-h-screen p-6'>
                <div className="flex justify-between items-center mb-6">
                    <h1 className="text-3xl font-bold">Dashboard</h1>
                </div>
                <BetDialog
                    key={selectedGame?.id}
                    selectedGame={selectedGame}
                    selectedBetType={selectedBetType}
                    onClose={handleCloseDialog}
                    onBetPlaced={refreshUser}
                />
                <div>
                    {
                        isLoading ? (
                            <p>Loading games...</p>
                        )
                            : errorMessage ? (
                                <p className="text-red-500">{errorMessage}</p>
                            ) : games.length === 0 ? (
                                <p>No upcoming games</p>
                            ) : (
                                games.map((game) => (
                                    <GameCard key={game.id} game={game} onBetClick={handleBetClick} />
                                ))
                            )
                    }
                </div>
            </div>
        </>
    )
}

export default Dashboard