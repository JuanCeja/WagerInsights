import axios from 'axios'

const API_BASE_URL = "http://localhost:8000"

export async function getLeaderBoard() {
    const response = await axios.get(`${API_BASE_URL}/auth/leaderboard`)
    return response.data
}