import axios from 'axios'

const API_BASE_URL = "http://localhost:8000"

export async function getCurrentUser() {
    const token = localStorage.getItem("token")
    const response = await axios.get(`${API_BASE_URL}/auth/me`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    })
    return response.data
}