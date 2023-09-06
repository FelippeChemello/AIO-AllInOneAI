from .PoeAPI import PoeApi

from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()

class Source(BaseModel):
    source_field: str 

class BingResponse(BaseModel):
    text: str
    author: str
    sources: List[Source]  # Use the defined Source model here
    sources_text: str
    suggestions: List[str]
    messages_left: int
    max_messages: int
    adaptive_text: str

@router.post(
    "/", 
    response_model=BingResponse, 
)
async def post():
    # try:
        client = PoeApi("gZ2cdMdknUMOwzecQ95Ffg%3D%3D")

        bot = "a2"
        message = "What is reverse engineering?"
        client.send_message(bot, message)
        print(client.get_latest_message(bot))

        return {"text": "Hello World"}
    # except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))