import { Button } from "@/components/ui/button.jsx"
import { useNavigate } from "react-router-dom"

function Dashboard() {
    const navigate = useNavigate()

    const handleLogout = () => {
        localStorage.removeItem("token")
        navigate("/login")
    }

    return (
        <div className='flex min-h-sreen items-center justify-center'>
            <h1 className='text-3xl font-bold'>Dashboard Page</h1>
            <Button onClick={handleLogout} variant="outline">Logout</Button>
        </div>
    )
}

export default Dashboard