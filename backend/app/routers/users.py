from app import crud, schemas
from app.auth import create_access_token, verify_password
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Router instance
router = APIRouter(
    prefix="/auth", # All routes in this router start with /auth
    tags=["Authentication"] # Groups these endpoints in /docs under "Authentication"
)

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
        Register a new user account.

        - **email**: Must be a valid email format
        - **username**: Unique username
        - **password**: At least 8 characters
        
        Returns the created user with a starting balance of 1000.0
    """
    
    # check if email already exists
    existing_user = crud.get_user_by_email(db, email = user.email)
    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail= "Email already registered"
        )
        
        
    existing_user = crud.get_user_by_username(db, username = user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )
        
    new_user = crud.create_user(db, user = user)
    
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    
    if not user:
        user = crud.get_user_by_username(db, username=form_data.username)
        
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    access_token = create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "Bearer"}