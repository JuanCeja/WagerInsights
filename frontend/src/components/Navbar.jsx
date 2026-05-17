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
        <nav>
            <h1>WagerInsights</h1>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/my-bets">My Bets</Link>
            <p>Balance: ${user?.balance?.toFixed(2)}</p>
            <Button onClick={handleLogout}>Logout</Button>
        </nav>
    )
}

export default Navbar