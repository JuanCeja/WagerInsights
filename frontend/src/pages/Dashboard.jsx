import GameCard from "@/components/GameCard"
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
                                <GameCard key={game.id} game={game} />
                            ))
                        )
                }
            </div>
        </div>
    )
}

export default Dashboard