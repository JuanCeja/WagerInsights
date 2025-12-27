from app import models, schemas
from app.auth import hash_password
from sqlalchemy.orm import Session

# USER CRUD OPERATIONS

def get_user_by_email(db: Session, email: str):
    """Get a user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """Get a user by username"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, id: int):
    """Get a user by ID"""
    return db.query(models.User).filter(models.User.id == id).first()