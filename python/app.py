import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

load_dotenv()

from services.elevenlabs.main import router as elevenlabs_router
from services.openai_plugin.main import router as openai_plugin_router
from services.llm.main import router as llm_router
from services.image_diffusion.main import router as image_diffusion_router
from services.aeneas.main import router as aeneas_router

app = FastAPI()

async def auth_middleware(request, call_next):
    allowed_api_keys = os.getenv("API_KEYS").split(",")
    api_key = request.headers.get("xi-api-key") if request.headers.get("xi-api-key") else request.query_params.get("xi-api-key")
    if not api_key:
        api_key = request.headers.get("Authorization").replace("Bearer ", "") if request.headers.get("Authorization") else None

    paths_without_auth = ["/", "/docs", "/openapi.json", "/redoc", "/openai-plugin/.well-known/ai-plugin.json", "/openai-plugin/.well-known/openapi.json"]
    path = request.url.path

    if path in paths_without_auth or (api_key and api_key in allowed_api_keys):
        return await call_next(request)
    else:
        return Response("Unauthorized", status_code=401)

app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)

@app.get("/")
def status():
    return {"status": "ok!!!"}

app.include_router(elevenlabs_router, prefix="/elevenlabs")
app.include_router(openai_plugin_router, prefix="/openai-plugin")
app.include_router(llm_router, prefix="/llm")
app.include_router(image_diffusion_router, prefix="/images")
app.include_router(aeneas_router, prefix="/aeneas")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
