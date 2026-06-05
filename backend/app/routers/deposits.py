from datetime import datetime

from app import auth, crud, models, schemas
from app.api_clients.stripe_client import create_payment_intent
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/deposits",
    tags=["Deposits"]
)

