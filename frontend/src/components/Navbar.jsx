import { Button } from "@/components/ui/button"
import { useUser } from "@/contexts/UserContext"
import { Link, useNavigate } from "react-router-dom"


const Navbar = () => {
    const { user } = useUser()
    const navigate = useNavigate()

    const handleLogout = () => {
        localStorage.removeItem("token")
        navigate("/login")
    }

    return (
<nav className="border-b">
    <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-6">
            <Link
                to="/"
                className="text-2xl tracking-tight hover:opacity-90 transition-opacity"
                style={{ fontFamily: "'Space Grotesk', sans-serif" }}
            >
                <span style={{ fontWeight: 700, color: '#a855f7' }}>Wager</span>
                <span style={{ fontWeight: 500 }}>Insights</span>
            </Link>
            <Link to="/dashboard" className="text-sm hover:underline">Dashboard</Link>
            <Link to="/leaderboard" className="text-sm hover:underline">Leaderboard</Link>
            {user && <Link to="/my-bets" className="text-sm hover:underline">My Bets</Link>}
            {user && <Link to="/deposit" className="text-sm hover:underline">Deposit</Link>}
        </div>

        <div className="flex items-center gap-4">
            {user ? (
                <>
                    <span className="text-sm font-medium">${user?.balance?.toFixed(2)}</span>
                    <Button onClick={handleLogout} variant="outline" size="sm">Logout</Button>
                </>
            ) : (
                <>
                    <Link to="/login"><Button variant="outline" size="sm">Login</Button></Link>
                    <Link to="/register"><Button size="sm">Register</Button></Link>
                </>
            )}
        </div>
    </div>
</nav>
    )
}

export default Navbar