import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useUser } from "@/contexts/UserContext"
import { login } from "@/services/authService"
import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"


function Login() {

    const navigate = useNavigate()

    const [usernameOrEmail, setUsernameOrEmail] = useState("")
    const [password, setPassword] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")

    const { refreshUser } = useUser()

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            setErrorMessage("")
            setIsLoading(true)
            const token = await login(usernameOrEmail, password)
            localStorage.setItem("token", token.access_token)
            await refreshUser()
            navigate("/dashboard")
        } catch (error) {
            setErrorMessage("Incorrect email/username or password")
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="flex min-h-screen items-center justify-center">
            <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-80">
                <h1 className="text-2xl font-bold">Login</h1>

                <div className="flex flex-col gap-2">
                    <Label htmlFor="identifier">Email or Username</Label>
                    <Input
                        id="identifier"
                        type="text"
                        value={usernameOrEmail}
                        onChange={(e) => setUsernameOrEmail(e.target.value)}
                    />
                </div>

                <div className="flex flex-col gap-2">
                    <Label htmlFor="password">Password</Label>
                    <Input
                        id="password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <Button type="submit" disabled={isLoading}>
                    {isLoading ? "Logging in..." : "Login"}
                </Button>

                <p className="text-sm text-center">
                    Don't have an account?{" "}
                    <Link to="/register" className="text-blue-500 underline">Sign up</Link>
                </p>

                {errorMessage && <p className="text-red-500">{errorMessage}</p>}
            </form>
        </div>
    )
}

export default Login