// frontend/src/components/DepositForm.jsx
import { Button } from "@/components/ui/button"
import { useUser } from "@/contexts/UserContext"
import { confirmDeposit } from "@/services/depositsService"
import { PaymentElement, useElements, useStripe } from "@stripe/react-stripe-js"
import { useState } from "react"

const DepositForm = ({ paymentIntentId, onProcessing, onSuccess, onError }) => {
    const stripe = useStripe()
    const elements = useElements()
    const { refreshUser } = useUser()
    const [isSubmitting, setIsSubmitting] = useState(false)

    const handlePay = async () => {
        if (!stripe || !elements) return

        setIsSubmitting(true)

        const { error } = await stripe.confirmPayment({
            elements,
            redirect: "if_required",
        })

        if (error) {
            onError(error.message || "Payment failed")
            setIsSubmitting(false)
            return
        }

        onProcessing()

        try {
            await confirmDeposit({ paymentIntentId })
            await refreshUser()
            onSuccess()
        } catch (backendError) {
            onError(backendError.response?.data?.detail || "Failed to credit deposit")
            setIsSubmitting(false)
        }
    }

    return (
        <div>
            <PaymentElement />
            <Button
                onClick={handlePay}
                disabled={!stripe || !elements || isSubmitting}
                className="mt-4 w-full"
            >
                {isSubmitting ? "Processing..." : "Pay"}
            </Button>
        </div>
    )
}

export default DepositForm