import { Button } from "@/components/ui/button"
import { useUser } from "@/contexts/UserContext"
import { Menu, X } from "lucide-react"
import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"


const Navbar = () => {
    const { user } = useUser()
    const navigate = useNavigate()
    const [menuOpen, setMenuOpen] = useState(false)

    const handleLogout = () => {
        localStorage.removeItem("token")
        setMenuOpen(false)
        navigate("/login")
    }

    return (
<nav className="relative border-b pt-[env(safe-area-inset-top)]">
    <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between gap-4">
        <div className="flex items-center gap-6">
            <Link
                to="/"
                className="text-2xl tracking-tight hover:opacity-90 transition-opacity whitespace-nowrap"
                style={{ fontFamily: "'Space Grotesk', sans-serif" }}
            >
                <span style={{ fontWeight: 700, color: '#a855f7' }}>Wager</span>
                <span style={{ fontWeight: 500 }}>Insights</span>
            </Link>
            <Link to="/dashboard" className="hidden md:inline text-sm hover:underline whitespace-nowrap">Dashboard</Link>
            <Link to="/leaderboard" className="hidden md:inline text-sm hover:underline whitespace-nowrap">Leaderboard</Link>
            {user && <Link to="/my-bets" className="hidden md:inline text-sm hover:underline whitespace-nowrap">My Bets</Link>}
            {user && <Link to="/deposit" className="hidden md:inline text-sm hover:underline whitespace-nowrap">Deposit</Link>}
        </div>

        <div className="flex items-center gap-4">
            {user ? (
                <>
                    <span className="text-sm font-medium whitespace-nowrap">${user?.balance?.toFixed(2)}</span>
                    <Button onClick={handleLogout} variant="outline" size="sm" className="hidden md:inline-flex">Logout</Button>
                </>
            ) : (
                <div className="hidden md:flex items-center gap-4">
                    <Link to="/login"><Button variant="outline" size="sm">Login</Button></Link>
                    <Link to="/register"><Button size="sm">Register</Button></Link>
                </div>
            )}

            <Button
                onClick={() => setMenuOpen((open) => !open)}
                variant="outline"
                size="icon"
                className="md:hidden size-11"
                aria-label={menuOpen ? "Close menu" : "Open menu"}
                aria-expanded={menuOpen}
            >
                {menuOpen ? <X /> : <Menu />}
            </Button>
        </div>
    </div>

    {menuOpen && (
        <div className="md:hidden absolute inset-x-0 top-full z-50 border-b bg-background shadow-md">
            <div className="flex flex-col px-6 py-2">
                <Link to="/dashboard" onClick={() => setMenuOpen(false)} className="flex items-center min-h-11 text-sm">Dashboard</Link>
                <Link to="/leaderboard" onClick={() => setMenuOpen(false)} className="flex items-center min-h-11 text-sm">Leaderboard</Link>
                {user && <Link to="/my-bets" onClick={() => setMenuOpen(false)} className="flex items-center min-h-11 text-sm">My Bets</Link>}
                {user && <Link to="/deposit" onClick={() => setMenuOpen(false)} className="flex items-center min-h-11 text-sm">Deposit</Link>}

                {user ? (
                    <Button onClick={handleLogout} variant="outline" size="sm" className="my-2 w-full min-h-11">Logout</Button>
                ) : (
                    <div className="flex flex-col gap-2 my-2">
                        <Link to="/login" onClick={() => setMenuOpen(false)}><Button variant="outline" size="sm" className="w-full min-h-11">Login</Button></Link>
                        <Link to="/register" onClick={() => setMenuOpen(false)}><Button size="sm" className="w-full min-h-11">Register</Button></Link>
                    </div>
                )}
            </div>
        </div>
    )}
</nav>
    )
}

export default Navbar