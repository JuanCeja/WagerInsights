import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function getLeaderBoard() {
    const response = await axios.get(`${API_BASE_URL}/auth/leaderboard`)
    return response.data
}