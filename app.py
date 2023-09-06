from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from services.elevenlabs.main import router as elevenlabs_router

app = FastAPI()


@app.get("/")
def status():
    return {"status": "ok"}


@app.get("/llm/models")
@app.get("/llm/v1/models")
def llm_models():
    return {}


app.include_router(elevenlabs_router, prefix="/elevenlabs")
