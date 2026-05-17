import { getCurrentUser } from "@/services/userService.js";
import { createContext, useContext, useEffect, useState } from "react";


const UserContext = createContext(null)


export function UserProvider({ children }) {
    const [user, setUser] = useState(null)
    const [isLoading, setIsLoading] = useState(true)

    async function refreshUser() {
        try {
            let currentUser = await getCurrentUser()
            setUser(currentUser)
        } catch (error) {
            localStorage.removeItem("token")
        } finally {
            setIsLoading(false)
        }
    }

    useEffect(() => {
        refreshUser()
    }, [])

    return (
        <UserContext.Provider value={{ user, isLoading, refreshUser }}>
            {children}
        </UserContext.Provider>
    )
}

export function useUser() {
    return useContext(UserContext)
}