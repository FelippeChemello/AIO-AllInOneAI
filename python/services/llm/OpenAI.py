from g4f import ChatCompletion, models
from datetime import datetime
from fastapi.responses import StreamingResponse, JSONResponse

from services.llm.LLM import LLM

class OpenAI(LLM):
    def __init__(self):
        super().__init__()

    def get_models(self):
        return [name for name in models.Model.__all__()]

    def generate(self, messages, model):
        return ChatCompletion.create(
            model=model,
            messages=messages,
        )
    

