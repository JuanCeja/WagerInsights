import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function getCurrentUser() {
    const token = localStorage.getItem("token")
    const response = await axios.get(`${API_BASE_URL}/auth/me`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    })
    return response.data
}