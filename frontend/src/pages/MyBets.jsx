import Navbar from "@/components/Navbar"
import { Button } from "@/components/ui/button.jsx"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useUser } from "@/contexts/UserContext"
import { getMyBets } from "@/services/betsService"
import { Ticket } from "lucide-react"
import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import {
    CartesianGrid,
    Cell,
    Legend,
    Line,
    LineChart,
    Pie,
    PieChart,
    ResponsiveContainer,
    Tooltip,
    XAxis, YAxis
} from "recharts"

const MyBets = () => {
    const [errorMessage, setErrorMessage] = useState("")
    const [userBets, setUserBets] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [activeTab, setActiveTab] = useState("all")

    const { user } = useUser()
    const userStartingBalance = 1000

    const filteredBets = activeTab === "all"
        ? userBets
        : userBets.filter(bet => bet.status === activeTab)

    const totalBets = userBets.length
    const totalWagered = userBets.reduce((sum, bet) => sum + bet.bet_amount, 0)
    const settledBets = userBets.filter(bet => bet.status === "won" || bet.status === "lost")
    const wonBets = userBets.filter(bet => bet.status === "won")
    const lostBets = userBets.filter((bet) => bet.status === "lost")

    const sortedUserBets = [...settledBets].sort((a, b) => new Date(a.game.game_date) - new Date(b.game.game_date))

    const balanceChartData = user
        ? sortedUserBets.reduce((chartData, bet) => {
            const previousBalance = chartData[chartData.length - 1].balance
            let newBalance = previousBalance

            if (bet.status === "won") {
                newBalance += (bet.potential_payout - bet.bet_amount)
            } else {
                newBalance -= bet.bet_amount
            }

            chartData.push({
                date: bet.game.game_date,
                balance: newBalance
            })
            return chartData
        }, [{
            date: user.created_at,
            balance: userStartingBalance
        }])
        : []

    const pieChartData = [
        {
            name: "Won",
            value: wonBets.length
        },
        {
            name: "Lost",
            value: lostBets.length
        }
    ]

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
            <div className="max-w-6xl mx-auto px-6 py-8">
                <h1 className="text-3xl font-bold mb-6">My Bets</h1>

                {isLoading && <p>Fetching Games</p>}
                {errorMessage && <p>{errorMessage}</p>}

                {/* Stats cards */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <Card>
                        <CardHeader className="pb-2">
                            <CardTitle className="text-xs uppercase tracking-wider text-muted-foreground font-medium">Total Bets</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-4xl font-bold font-mono">{totalBets}</p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader className="pb-2">
                            <CardTitle className="text-xs uppercase tracking-wider text-muted-foreground font-medium">Total Wagered</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-4xl font-bold font-mono">${totalWagered.toFixed(2)}</p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader className="pb-2">
                            <CardTitle className="text-xs uppercase tracking-wider text-muted-foreground font-medium">Win Rate</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-4xl font-bold font-mono">{winRate.toFixed(1)}%</p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader className="pb-2">
                            <CardTitle className="text-xs uppercase tracking-wider text-muted-foreground font-medium">Net P/L</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className={`text-4xl font-bold font-mono ${netProfitLoss >= 0 ? "text-green-600" : "text-red-500"}`}>
                                ${netProfitLoss.toFixed(2)}
                            </p>
                        </CardContent>
                    </Card>
                </div>

                {/* Win/Loss Pie Chart */}
                {settledBets.length > 0 &&
                    (<Card className="mb-6">
                        <CardHeader>
                            <CardTitle className="text-sm text-gray-500">Win / Loss Breakdown</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <ResponsiveContainer width="100%" height={250}>
                                <PieChart>
                                    <Pie
                                        data={pieChartData}
                                        dataKey="value"
                                        nameKey="name"
                                        cx="50%"
                                        cy="50%"
                                        outerRadius={80}
                                        label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
                                    >
                                        {pieChartData.map((entry) => (
                                            <Cell
                                                key={entry.name}
                                                fill={entry.name === "Won" ? "#a855f7" : "#475569"}
                                            />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                    <Legend />
                                </PieChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>)}

                {/* Balance Over Time */}
                {balanceChartData.length > 1 && (
                    <Card className="mb-6">
                        <CardHeader>
                            <CardTitle className="text-sm text-gray-500">Balance Over Time</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <ResponsiveContainer width="100%" height={300}>
                                <LineChart data={balanceChartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                    <XAxis
                                        dataKey="date"
                                        stroke="#94a3b8"
                                        tickFormatter={(d) => new Date(d).toLocaleDateString(undefined, { month: "short", day: "numeric" })}
                                    />
                                    <YAxis
                                        stroke="#94a3b8"
                                        domain={["dataMin - 50", "dataMax + 50"]}
                                        tickFormatter={(v) => `$${v.toFixed(0)}`}
                                    />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: "#1e293b", border: "1px solid #334155" }}
                                        labelFormatter={(d) => new Date(d).toLocaleString()}
                                        formatter={(v) => [`$${v.toFixed(2)}`, "Balance"]}
                                    />
                                    <Line
                                        type="monotone"
                                        dataKey="balance"
                                        stroke="#a855f7"
                                        strokeWidth={2}
                                        dot={{ r: 3, fill: "#a855f7" }}
                                        activeDot={{ r: 5 }}
                                    />
                                </LineChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                )}

                {/* Tabs */}
                <Tabs value={activeTab} onValueChange={setActiveTab}>
                    <TabsList>
                        <TabsTrigger value="all">All</TabsTrigger>
                        <TabsTrigger value="pending">Pending</TabsTrigger>
                        <TabsTrigger value="won">Won</TabsTrigger>
                        <TabsTrigger value="lost">Lost</TabsTrigger>
                    </TabsList>

                    <TabsContent value={activeTab} className="mt-4">
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
                                    <div key={bet.id} className="border rounded-lg p-4 mb-4 hover:shadow-md hover:border-primary/30 hover:-translate-y-1 transition-all">
                                        <div className="flex items-center justify-between mb-2">
                                            <p className="font-semibold">{bet.game.away_team} @ {bet.game.home_team}</p>
                                            <span className={`text-sm font-semibold capitalize ${statusColor(bet.status)}`}>
                                                {bet.status}
                                            </span>
                                        </div>

                                        <p className="text-sm text-gray-500 mb-3">
                                            {bet.game.sport} • {new Date(bet.game.game_date).toLocaleString()}
                                        </p>

                                        <div className="flex justify-between text-sm">
                                            <div>
                                                <span className="text-gray-500">Pick: </span>
                                                <span className="font-medium">{teamBetOn}</span>
                                                <span className="text-gray-400"> ({bet.odds_at_bet > 0 ? `+${bet.odds_at_bet}` : bet.odds_at_bet})</span>
                                            </div>
                                            <div>
                                                <span className="text-gray-500">Wager: </span>
                                                <span className="font-medium">${bet.bet_amount}</span>
                                            </div>
                                        </div>

                                        {bet.status === "won" && (
                                            <p className="text-sm text-green-600 font-medium mt-2">
                                                Payout: ${bet.potential_payout.toFixed(2)} (+${(bet.potential_payout - bet.bet_amount).toFixed(2)} profit)
                                            </p>
                                        )}

                                        {bet.status === "lost" && (
                                            <p className="text-sm text-red-500 font-medium mt-2">
                                                Lost: ${bet.bet_amount.toFixed(2)}
                                            </p>
                                        )}
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