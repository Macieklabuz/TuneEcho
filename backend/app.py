from flask import Flask, jsonify
from flask_cors import CORS
from .database import init_db

app = Flask(__name__)
CORS(app)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/init")
def init():
    init_db()
    return {"status": "db initialized"}
