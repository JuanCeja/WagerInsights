from datetime import datetime

import stripe
from app import auth, crud, models, schemas
from app.api_clients.stripe_client import (create_payment_intent,
                                           retrieve_payment_intent)
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/deposits",
    tags=["Deposits"]
)

@router.post(
        "/create-intent", 
        response_model=schemas.DepositCreateResponse, 
        status_code=status.HTTP_201_CREATED
)
def create_intent(
    body: schemas.DepositCreateRequest, 
    current_user: models.User = Depends(auth.get_current_user)
    ):
    intent = create_payment_intent(amount=body.amount, user_id=current_user.id)
    return schemas.DepositCreateResponse(
        payment_intent_id=intent["id"],
        client_secret=intent["client_secret"]
    )

@router.post(
    "/confirm",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_200_OK
    )
def confirm_deposit(
    body: schemas.DepositConfirmRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    try:
        intent = retrieve_payment_intent(body.payment_intent_id)
    except stripe.error.InvalidRequestError:
        raise HTTPException(status_code=404, detail="Payment intent not found")
    except stripe.error.StripeError:
        raise HTTPException(status_code=502, detail="Stripe service error")

    if intent["status"] != "succeeded":
        raise HTTPException(status_code=400, detail="Payment did not succeed")
    
    if int(intent["metadata"]["user_id"]) != current_user.id:
        raise HTTPException(status_code=403, detail="Payment intent does not belong to this user")
    
    existing = crud.get_deposit_by_stripe_id(db, body.payment_intent_id)

    if existing:
        db.refresh(current_user)
        return current_user
    
    amount_dollars = intent["amount"] / 100

    updated_user = crud.create_deposit_and_credit_user(
        db,
        amount=amount_dollars,
        user_id=current_user.id,
        stripe_payment_intent_id=body.payment_intent_id,
    )

    return updated_user