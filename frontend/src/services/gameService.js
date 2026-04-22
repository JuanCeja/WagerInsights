import axios from 'axios'

const API_BASE_URL = "http://localhost:8000"

export async function getGames() {
    const response = await axios.get(`${API_BASE_URL}/games`, {
        params: { status }
    })
    return response.data
}