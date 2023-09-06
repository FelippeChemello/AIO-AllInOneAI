import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

load_dotenv()

from services.elevenlabs.main import router as elevenlabs_router

app = FastAPI()


async def auth_middleware(request, call_next):
    allowed_api_keys = os.getenv("API_KEYS").split(",")
    api_key = request.headers.get("xi-api-key") if request.headers.get("xi-api-key") else request.query_params.get("xi-api-key")

    if api_key and api_key in allowed_api_keys:
        return await call_next(request)
    else:
        return Response("Unauthorized", status_code=401)


app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)


@app.get("/")
def status():
    return {"status": "ok!"}


@app.get("/llm/models")
@app.get("/llm/v1/models")
def llm_models():
    return {}


app.include_router(elevenlabs_router, prefix="/elevenlabs")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
