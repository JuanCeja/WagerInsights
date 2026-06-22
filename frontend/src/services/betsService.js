import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function placeBet({ gameId, betType, betAmount }) {
    const token = localStorage.getItem("token")
    const response = await axios.post(`${API_BASE_URL}/bets`,
        {
            game_id: gameId,
            bet_type: betType,
            bet_amount: betAmount
        },
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })
    return response.data
}

export async function getMyBets({ status, betType } = {}) {
    const token = localStorage.getItem("token")
    const response = await axios.get(`${API_BASE_URL}/bets`,
        {
            params: { status, bet_type: betType },

            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    )
    return response.data
}

export async function analyzeBet({ gameId, betType, betAmount }) {
    const token = localStorage.getItem("token")
    const response = await axios.post(
        `${API_BASE_URL}/bets/analyze`,
        {
            game_id: gameId,
            bet_type: betType,
            bet_amount: betAmount
        },
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    )
    return response.data
}