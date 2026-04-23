import { Button } from "@/components/ui/button.jsx"
import { getGames } from "@/services/gamesService"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

function Dashboard() {
    const [games, setGames] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [errorMessage, setErrorMessage] = useState("")

    const navigate = useNavigate()

    useEffect(() => {
        async function fetchGames() {
            try {
                const data = await getGames({status: "upcoming"})
                setGames(data)
            } catch (error) {
                setErrorMessage("There is an issue retrieving games")
            } finally {
                setIsLoading(false)
            }
        }

        fetchGames()
    }, [])

    const handleLogout = () => {
        localStorage.removeItem("token")
        navigate("/login")
    }

    return (
        <div className='min-h-screen p-6'>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">Dashboard</h1>
                <Button onClick={handleLogout} variant="outline">Logout</Button>
            </div>
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
                                <div key={game.id} className="border rounded-lg p-4">
                                    <p className="font-semibold">{game.away_team} @ {game.home_team}</p>
                                    <p className="text-sm text-gray-600">{game.sport} • {new Date(game.game_date).toLocaleString()}</p>
                                    <div className="flex gap-4 mt-2">
                                        <span>Home: {game.home_team_odds > 0 ? `+${game.home_team_odds}` : game.home_team_odds}</span>
                                        <span>Away: {game.away_team_odds > 0 ? `+${game.away_team_odds}` : game.away_team_odds}</span>
                                    </div>
                                </div>
                            ))
                        )
                }
            </div>
        </div>
    )
}

export default Dashboard