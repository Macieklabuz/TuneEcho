from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.database.database import init_db

app = FastAPI(title="TuneEcho API", version="1.0.0")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  
    yield 

# ----- Endpoints -----
@app.get("/")
def home():
    return {"message": "Hello from FastAPI 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

