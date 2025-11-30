from app import models
from app.database import Base, engine
from fastapi import FastAPI

Base.metadata.create_all(bind = engine)

app = FastAPI(title="WagerInsights API", version = "1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to WagerInsights API"}

@app.get("/health")
def health_check():
    return {"status": "Healthy"}