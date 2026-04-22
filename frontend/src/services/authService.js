import axios from 'axios'

const API_BASE_URL = "http://localhost:8000"

export async function login(usernameOrEmail, password) {
    const formData = new URLSearchParams()
    formData.append("username", usernameOrEmail)
    formData.append("password", password)

    const response = await axios.post(
        `${API_BASE_URL}/auth/login`,
        formData,
        {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        }
    )

    return response.data
}

export async function register(username, email, password) {
    const formData = { username, email, password }

    const response = await axios.post(
        `${API_BASE_URL}/auth/register`,
        formData
    )

    return response.data
}