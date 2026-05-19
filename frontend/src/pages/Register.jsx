import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useUser } from "@/contexts/UserContext"
import { login, register } from "@/services/authService"
import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"

const Register = () => {
    const navigate = useNavigate()

    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")

    const { refreshUser } = useUser()

    const handleSubmit = async (e) => {
        e.preventDefault()

        try {
            setErrorMessage("")
            setIsLoading(true)
            const user = await register(username, email, password)
            const token = await login(user.username, password)
            localStorage.setItem("token", token.access_token)
            await refreshUser()
            navigate("/dashboard")
        } catch (error) {
            setErrorMessage("Registration failed. Please try again")
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="flex min-h-screen items-center justify-center">
            <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-80">
                <h1 className="text-2xl font-bold">Create Account</h1>

                <div className="flex flex-col gap-2">
                    <Label htmlFor="username">Username</Label>
                    <Input
                        id="username"
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>

                <div className="flex flex-col gap-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                        id="email"
                        type="text"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
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
                    {isLoading ? "Creating Account..." : "Create Account"}
                </Button>

                <p className="text-sm text-center">
                    Already have an account?{" "}
                    <Link to="/login" className="text-blue-500 underline">Log in</Link>
                </p>

                {errorMessage && <p className="text-red-500">{errorMessage}</p>}
            </form>
        </div>
    )
}

export default Register