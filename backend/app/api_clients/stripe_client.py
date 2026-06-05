import os

import stripe

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

def create_payment_intent(amount: float, user_id: int):
    intent = stripe.PaymentIntent.create(
        amount=int(round(amount * 100)),
        currency="usd",
        metadata={
            "user_id": user_id,
        },
    )

    return {
        "id": intent.id,
        "client_secret": intent.client_secret,
        "status": intent.status,
        "metadata": intent.metadata,
    }