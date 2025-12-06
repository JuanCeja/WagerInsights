import os
from datetime import datetime, timedelta
from typing import Optional

from app import models, schemas
from app.database import get_db
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

load_dotenv()

