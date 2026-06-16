import DepositForm from "@/components/DepositForm"
import Navbar from "@/components/Navbar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useUser } from "@/contexts/UserContext"
import { createPaymentIntent } from "@/services/depositsService"
import { Elements } from "@stripe/react-stripe-js"
import { loadStripe } from "@stripe/stripe-js"
import { CheckCircle2, Loader2 } from "lucide-react"
import { useState } from "react"
import { Link } from "react-router-dom"



const Deposit = () => {
    const [stage, setStage] = useState("amount")
    const [clientSecret, setClientSecret] = useState("")
    const [paymentIntentId, setPaymentIntentId] = useState("")
    const [selectedAmount, setSelectedAmount] = useState(0)
    const [errorMessage, setErrorMessage] = useState("")

    const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY)


    const { refreshUser, user } = useUser()

    const amounts = [25, 50, 100, 200]

    const handleContinue = async () => {
        try {
            setErrorMessage("")
            const data = await createPaymentIntent({ amount: selectedAmount })
            setClientSecret(data.client_secret)
            setPaymentIntentId(data.payment_intent_id)
            setStage("card")
        } catch (error) {
            setErrorMessage(error.response?.data?.detail || "Failed to start deposit")
        }
    }

    return (
        <div>
            <Navbar />

            {/* initial/amount stage */}
            {stage === "amount" && (
                <div>
                    <Input
                        type="number"
                        placeholder="Enter custom amount"
                        value={selectedAmount}
                        onChange={(e) => setSelectedAmount(parseFloat(e.target.value) || 0)}
                    />

                    {amounts.map((amount) => (
                        <Button key={amount} onClick={() => setSelectedAmount(amount)}>
                            ${amount}
                        </Button>
                    ))}

                    <Button onClick={handleContinue} disabled={selectedAmount === 0}>
                        Continue
                    </Button>

                    {errorMessage && <p className="text-red-500">{errorMessage}</p>}
                </div>
            )}

            {/* card stage */}
            {stage === "card" && (
                <Elements
                    stripe={stripePromise}
                    options={{
                        clientSecret,
                        appearance: {
                            theme: "night",
                            variables: {
                                colorPrimary: "#a855f7",
                                colorBackground: "#0f172a",
                                colorText: "#e2e8f0",
                                borderRadius: "8px",
                            },
                        },
                    }}
                >
                    <DepositForm
                        paymentIntentId={paymentIntentId}
                        onProcessing={() => setStage("processing")}
                        onSuccess={() => setStage("success")}
                        onError={(msg) => setErrorMessage(msg)}
                    />
                </Elements>
            )}
            
            {/* processing stage */}
            {stage === "processing" && (
                <div className="flex flex-col items-center justify-center py-12">
                    <Loader2 className="h-10 w-10 animate-spin text-primary mb-4" />
                    <p className="text-muted-foreground">Crediting your balance...</p>
                </div>
            )}

            {/* success stage */}
            {stage === "success" && (
                <div className="flex flex-col items-center justify-center py-12">
                    <CheckCircle2 className="h-14 w-14 text-green-500 mb-4" />
                    <h2 className="text-2xl font-bold mb-2">Deposit Successful!</h2>
                    <p className="text-muted-foreground mb-1">
                        ${selectedAmount.toFixed(2)} added to your balance
                    </p>
                    <p className="text-lg font-semibold mb-6">
                        New Balance: ${user?.balance?.toFixed(2)}
                    </p>
                    <div className="flex gap-3">
                        <Link to="/dashboard">
                            <Button>Back to Dashboard</Button>
                        </Link>
                        <Button
                            variant="outline"
                            onClick={() => {
                                setStage("amount")
                                setSelectedAmount(0)
                                setClientSecret("")
                                setPaymentIntentId("")
                                setErrorMessage("")
                            }}
                        >
                            Deposit Again
                        </Button>
                    </div>
                </div>
            )}
        </div>
    )
}

export default Deposit