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

    return (
        <>
        <Navbar />
            <h1>My Bets</h1>

            {isLoading && <p>Fetching Games</p>}

            {
                errorMessage ? <p>{errorMessage}</p>
                    : userBets.map((bet) => (
                        <div key={bet.id}>
                            <h3>Bet Id: {bet.id}</h3>
                            <p>Bet Amount: ${bet.bet_amount}</p>
                            <p>Status: {bet.status}</p>
                            <p>Odds At Bet: {bet.odds_at_bet}</p>
                            <p>Bet Created: {bet.created_at}</p>
                        </div>
                    ))
            }
        </>
    )
}

export default MyBets