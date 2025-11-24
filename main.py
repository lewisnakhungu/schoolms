from fastapi import FastAPI
from routes import auth, dashboard
from models.user import Base
from database import engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SchoolMS - Python FastAPI Version")

app.include_router(auth.router)
app.include_router(dashboard.router)

@app.get("/")
def home():
    return {"message": "SchoolMS FastAPI backend - Day 1 complete!"}