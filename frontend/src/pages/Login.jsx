import { useState } from "react"

function Login() {

    const [usernameOrEmail, setUsernameOrEmail] = useState("")
    const [password, setPassword] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")

    const handleSubmit = (e) => {
        e.preventDefault()
        console.log("From submitted:", { usernameOrEmail, password })
    }

    return (
        <div className="flex min-h-screen items-center justify-center">
            <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-80">
                <h1 className="text-2xl font-bold">Login</h1>

                <input
                    type="text"
                    placeholder="Email or Username"
                    value={usernameOrEmail}
                    onChange={(e) => setUsernameOrEmail(e.target.value)}
                    className="border p-2 rounded"
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="border p-2 rounded"
                />

                <button type="submit" className="bg-black text-white p-2 rounded">
                    Login
                </button>

                {errorMessage && <p className="text-red-500">{errorMessage}</p>}
            </form>
        </div>
    )
}

export default Login