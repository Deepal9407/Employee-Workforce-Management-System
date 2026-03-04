from fastapi import FastAPI
from backend.main import app as main_app

app = FastAPI()
app.mount("/api", main_app)
