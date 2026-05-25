from app import crud, models, schemas
from app.auth import create_access_token, get_current_user, verify_password
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func, case

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


@router.get("/me", response_model = schemas.UserResponse)
def get_current_user_profile(current_user: models.User = Depends(get_current_user)):
    """
    Get the currently logged-in user's profile.
    
    Requires valid JWT token in Authorization header.
    """
    return current_user

@router.get("/leaderboard", response_model=list[schemas.LeaderBoardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    leaderboard = []
    
    results = (
        db.query(
            models.User,
            func.count(case((models.Bet.status == "won", 1))).label("won_bets"),
            func.count(case((models.Bet.status != "pending", 1))).label("total_settled_bets")
        )
        .outerjoin(models.Bet, models.Bet.user_id == models.User.id)
        .group_by(models.User.id).all())
    
    for row in results:
        user = row.User
        won = row.won_bets
        total = row.total_settled_bets
        
        if total == 0:
            win_rate = 0
        else:
            win_rate = (won / total) * 100
            
        leaderboard.append(schemas.LeaderBoardEntry(
            username = user.username,
            balance = user.balance,
            win_rate = win_rate,
            total_bets = total
        ))
        
    leaderboard.sort(key = lambda e: (e.win_rate, e.total_bets), reverse = True)
    
    return leaderboard