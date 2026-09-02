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

export async function streamBetAnalysis({ gameId, betType, betAmount }, onChunk) {
    const token = localStorage.getItem("token")
    const response = await fetch(`${API_BASE_URL}/bets/analyze`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
            game_id: gameId,
            bet_type: betType,
            bet_amount: betAmount,
        }),
    })

    if (!response.ok) {
        let detail = "Failed to fetch bet analysis"
        try {
            const data = await response.json()
            detail = data.detail || detail
        } catch {
            // response body wasn't JSON, keep default message
        }
        throw new Error(detail)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
        const { done, value } = await reader.read()
        if (done) break
        onChunk(decoder.decode(value, { stream: true }))
    }
}