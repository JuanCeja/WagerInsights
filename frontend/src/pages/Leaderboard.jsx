// frontend/src/pages/Leaderboard.jsx
import Navbar from "@/components/Navbar"
import { getLeaderBoard } from "@/services/leaderBoardService"
import { Medal, Trophy } from "lucide-react"
import { useEffect, useState } from "react"

const Leaderboard = () => {
    const [isLoading, setIsLoading] = useState(true)
    const [leaderboard, setLeaderboard] = useState([])
    const [errorMessage, setErrorMessage] = useState("")

    useEffect(() => {
        async function fetchLeaderboard() {
            try {
                const data = await getLeaderBoard()
                setLeaderboard(data)
            } catch (error) {
                setErrorMessage("There is an issue retrieving the leaderboard")
            } finally {
                setIsLoading(false)
            }
        }

        fetchLeaderboard()
    }, [])

    return (
        <>
            <Navbar />

            <div className="max-w-6xl mx-auto px-6 py-8">
                <div className="flex items-center gap-2 mb-6">
                    <Trophy className="h-7 w-7 text-primary" />
                    <h1 className="text-3xl font-bold">Leaderboard</h1>
                </div>

                {isLoading ? (
                    <p className="text-muted-foreground">Fetching leaderboard...</p>
                ) : errorMessage ? (
                    <p className="text-red-500">{errorMessage}</p>
                ) : leaderboard.length === 0 ? (
                    <div className="text-center py-12">
                        <Trophy className="mx-auto h-12 w-12 text-gray-400" />
                        <h3 className="mt-4 text-lg font-semibold">No users yet</h3>
                        <p className="text-gray-500 mt-1">Be the first to place a bet and climb the board.</p>
                    </div>
                ) : (
                    <div className="rounded-lg border overflow-hidden">
                        <table className="w-full text-sm">
                            <thead className="bg-muted/50">
                                <tr className="text-left">
                                    <th className="px-4 py-3 font-semibold w-16">Rank</th>
                                    <th className="px-4 py-3 font-semibold">Player</th>
                                    <th className="px-4 py-3 font-semibold text-right">Win Rate</th>
                                    <th className="px-4 py-3 font-semibold text-right">Bets</th>
                                    <th className="px-4 py-3 font-semibold text-right">Balance</th>
                                </tr>
                            </thead>
                            <tbody>
                                {leaderboard.map((entry, index) => (
                                    <tr
                                        key={entry.username}
                                        className={`border-t hover:bg-muted/30 transition-colors ${index < 3 ? "bg-muted/10" : ""}`}
                                    >
                                        <td className="px-4 py-3">
                                            {index === 0 && <Trophy className="h-4 w-4 text-amber-400" />}
                                            {index === 1 && <Medal className="h-4 w-4 text-slate-400" />}
                                            {index === 2 && <Medal className="h-4 w-4 text-amber-600" />}
                                            {index > 2 && <span className="font-medium text-muted-foreground">{index + 1}</span>}
                                        </td>
                                        <td className="px-4 py-3 font-medium">{entry.username}</td>
                                        <td className="px-4 py-3 text-right">
                                            {entry.win_rate.toFixed(1)}%
                                        </td>
                                        <td className="px-4 py-3 text-right text-muted-foreground">
                                            {entry.total_bets}
                                        </td>
                                        <td className="px-4 py-3 text-right font-medium">
                                            ${entry.balance.toFixed(2)}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </>
    )
}

export default Leaderboard