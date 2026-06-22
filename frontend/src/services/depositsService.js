import axios from "axios"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function createPaymentIntent({ amount }) {
    const token = localStorage.getItem("token")
    const response = await axios.post(
        `${API_BASE_URL}/deposits/create-intent`,
        { amount },
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    )
    return response.data
}

export async function confirmDeposit({ paymentIntentId }) {
    const token = localStorage.getItem("token")
    const response = await axios.post(
        `${API_BASE_URL}/deposits/confirm`,
        { payment_intent_id: paymentIntentId },
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    )
    return response.data
}