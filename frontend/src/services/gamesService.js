import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function getGames(filters = {}) {
    const response = await axios.get(`${API_BASE_URL}/games`, {
        params: filters,
    })
    return response.data
}