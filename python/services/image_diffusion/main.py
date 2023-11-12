from fastapi import APIRouter

from services.image_diffusion.Playground import Playground

router = APIRouter()

playground = Playground()

@router.post("/v1/images/generations")
async def generate_image(req: dict):
    return await playground.generate_image(req["prompt"])