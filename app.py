from dotenv import load_dotenv
from fastapi import FastAPI

from services import poe_client

app = FastAPI()

@app.get("/")
def status():
    return { "status": "ok" }

@app.get('/models')
@app.get('/v1/models')
def models():
    return {}

app.include_router(poe_client.router, prefix="/poe", tags=["poe"])