import BetDialog from "@/components/BetDialog"
import GameCard from "@/components/GameCard"
import { Button } from "@/components/ui/button.jsx"
import { getGames } from "@/services/gamesService"
import { getCurrentUser } from "@/services/userService"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

function Dashboard() {
    const [games, setGames] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [errorMessage, setErrorMessage] = useState("")
    const [user, setUser] = useState(null)
    const [selectedGame, setSelectedGame] = useState(null)
    const [selectedBetType, setSelectedBetType] = useState(null)

    const navigate = useNavigate()

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

        async function getCurrentUserLoggedIn() {
            try {
                const userData = await getCurrentUser()
                setUser(userData)
            } catch (error) {
                localStorage.removeItem("token")
                navigate("/login")
            }

        }

        fetchGames()
        getCurrentUserLoggedIn()
    }, [])

    const handleLogout = () => {
        localStorage.removeItem("token")
        navigate("/login")
    }

    const handleBetClick = (game, betType) => {
        setSelectedGame(game)
        setSelectedBetType(betType)
    }

    const handleCloseDialog = () => {
        setSelectedGame(null)
        setSelectedBetType(null)
    }

    return (
        <div className='min-h-screen p-6'>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">Dashboard</h1>
                <p>${user?.balance?.toFixed(2)}</p>
                <Button onClick={handleLogout} variant="outline">Logout</Button>
            </div>
            <BetDialog
                key={selectedGame?.id}
                selectedGame={selectedGame}
                selectedBetType={selectedBetType}
                onClose={handleCloseDialog}
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
    )
}

export default Dashboard