from fastapi import APIRouter

from services.llm.OpenAI import OpenAI

router = APIRouter()

open_ai = OpenAI()


@router.get("/v1/models")
def get_models():
    return open_ai.get_models()

@router.post("/v1/chat/completions")
def completion(req: dict):
    return open_ai.generate(req["messages"], req["model"])
