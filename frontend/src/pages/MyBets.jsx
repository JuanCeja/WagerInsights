import Navbar from "@/components/Navbar"
import { getMyBets } from "@/services/betsService"
import { useEffect, useState } from "react"

const MyBets = () => {
    const [errorMessage, setErrorMessage] = useState("")
    const [userBets, setUserBets] = useState([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        async function fetchUserBets() {
            try {
                setIsLoading(true)
                const data = await getMyBets({})
                setUserBets(data)
            } catch (error) {
                setErrorMessage("Failed to load bets")
            } finally {
                setIsLoading(false)
            }
        }
        fetchUserBets()
    }, [])

    const statusColor = (status) => {
        if (status === "won") return "text-green-600"
        if (status === "lost") return "text-red-500"
        if (status === "pending") return "text-gray-500"
        return "text-gray-400"
    }

    return (
        <>
            <Navbar />
            <h1>My Bets</h1>

            {isLoading && <p>Fetching Games</p>}

            {
                errorMessage ? <p>{errorMessage}</p>
                    : userBets.map((bet) => {

                        const teamBetOn = bet.bet_type === "home"
                            ? bet.game.home_team
                            : bet.game.away_team

                        return (<div key={bet.id}>
                            <h3>Game Matchup: {bet.game.away_team} @ {bet.game.home_team}</h3>
                            <p>{new Date(bet.game.game_date).toLocaleString()}</p>
                            <p>{bet.game.sport}</p>
                            <p>Team bet on: {teamBetOn}</p>
                            <p>Bet Amount: ${bet.bet_amount}</p>
                            <p>Odds At Bet: {bet.odds_at_bet}</p>
                            <p className={`capitalize ${statusColor(bet.status)}`}>
                                Status: {bet.status}
                            </p>
                        </div>)
                    })
            }
        </>
    )
}

export default MyBets