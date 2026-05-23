import Navbar from "@/components/Navbar"
import { Button } from "@/components/ui/button.jsx"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getMyBets } from "@/services/betsService"
import { Ticket } from "lucide-react"
import { useEffect, useState } from "react"
import { Link } from "react-router-dom"

const MyBets = () => {
    const [errorMessage, setErrorMessage] = useState("")
    const [userBets, setUserBets] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [activeTab, setActiveTab] = useState("all")

    const filteredBets = activeTab === "all"
        ? userBets
        : userBets.filter(bet => bet.status === activeTab)

    const totalBets = userBets.length
    const totalWagered = userBets.reduce((sum, bet) => sum + bet.bet_amount, 0)

    const settledBets = userBets.filter(bet => bet.status === "won" || bet.status === "lost")
    const wonBets = userBets.filter(bet => bet.status === "won")
    const winRate = settledBets.length > 0
        ? (wonBets.length / settledBets.length) * 100
        : 0

    const netProfitLoss = userBets.reduce((net, bet) => {
        if (bet.status === "won") {
            return net + (bet.potential_payout - bet.bet_amount)
        }
        if (bet.status === "lost") {
            return net - bet.bet_amount
        }
        return net
    }, 0)

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
            <div className="p-6">
                <h1 className="text-3xl font-bold mb-6">My Bets</h1>

                {isLoading && <p>Fetching Games</p>}
                {errorMessage && <p>{errorMessage}</p>}

                {/* Stats cards — ONLY these are in the grid */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-sm text-gray-500">Total Bets</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-2xl font-bold">{totalBets}</p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-sm text-gray-500">Total Wagered</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-2xl font-bold">${totalWagered.toFixed(2)}</p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-sm text-gray-500">Win Rate</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-2xl font-bold">{winRate.toFixed(1)}%</p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-sm text-gray-500">Net Profit/Loss</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className={`text-2xl font-bold ${netProfitLoss >= 0 ? "text-green-600" : "text-red-500"}`}>
                                ${netProfitLoss.toFixed(2)}
                            </p>
                        </CardContent>
                    </Card>
                </div>

                {/* Tabs — ONE Tabs, containing both TabsList and TabsContent */}
                <Tabs value={activeTab} onValueChange={setActiveTab}>
                    <TabsList>
                        <TabsTrigger value="all">All</TabsTrigger>
                        <TabsTrigger value="pending">Pending</TabsTrigger>
                        <TabsTrigger value="won">Won</TabsTrigger>
                        <TabsTrigger value="lost">Lost</TabsTrigger>
                    </TabsList>

                    <TabsContent value={activeTab}>
                        {filteredBets.length === 0 ? (
                            <div className="text-center py-12">
                                <Ticket className="mx-auto h-12 w-12 text-gray-400" />
                                <h3 className="mt-4 text-lg font-semibold">No bets yet</h3>
                                <p className="text-gray-500 mt-1">Place your first bet to see it here.</p>
                                <Link to="/dashboard">
                                    <Button className="mt-4">Browse Games</Button>
                                </Link>
                            </div>
                        ) : (
                            filteredBets.map((bet) => {
                                const teamBetOn = bet.bet_type === "home"
                                    ? bet.game.home_team
                                    : bet.game.away_team

                                return (
                                    <div key={bet.id}>
                                        <h3>Game Matchup: {bet.game.away_team} @ {bet.game.home_team}</h3>
                                        <p>{new Date(bet.game.game_date).toLocaleString()}</p>
                                        <p>{bet.game.sport}</p>
                                        <p>Team bet on: {teamBetOn}</p>
                                        <p>Bet Amount: ${bet.bet_amount}</p>
                                        <p>Odds At Bet: {bet.odds_at_bet}</p>
                                        <p className={`capitalize ${statusColor(bet.status)}`}>
                                            Status: {bet.status}
                                        </p>
                                    </div>
                                )
                            })
                        )}
                    </TabsContent>
                </Tabs>
            </div>
        </>
    )
}

export default MyBets