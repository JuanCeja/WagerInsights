from app.database import Base, engine
from app.routers import users
from fastapi import FastAPI

Base.metadata.create_all(bind = engine)

app = FastAPI(title="WagerInsights API", description="Sports betting tracker with virtual money", version = "1.0.0")

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to WagerInsights API"}

@app.get("/health")
def health_check():
    return {"status": "Healthy"}