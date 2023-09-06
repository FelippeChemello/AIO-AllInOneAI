import os
import requests
import io
from fastapi.responses import StreamingResponse, JSONResponse

from services.elevenlabs.TTS import TTS


class ElevenLabsTTS(TTS):
    def __init__(self):
        super().__init__()

        self.base_url = "https://api.elevenlabs.io"
        self.users = os.getenv("ELEVEN_LABS_API_KEYS").split(",")

    def get_user(self, api_key):
        return requests.get(
            self.base_url + "/v1/user", headers={"xi-api-key": api_key}
        ).json()

    def get_usage(self, api_key):
        user = self.get_user(api_key)
        return {
            "usage": user["subscription"]["character_count"],
            "limit": user["subscription"]["character_limit"],
        }

    def get_all_usage(self):
        return [self.get_usage(api_key) for api_key in self.users]

    def get_api_key(self, need_character_count):
        for api_key in self.users:
            usage = self.get_usage(api_key)
            if usage["usage"] + need_character_count < usage["limit"]:
                return api_key

    def get_voices(self):
        return requests.get(self.base_url + "/v1/voices").json()

    def synthesize(self, voice, req):
        response = requests.post(
            self.base_url + "/v1/text-to-speech/" + voice,
            json=req,
            headers={"xi-api-key": None},
        )

        if response.status_code == 200:
            audio_data = response.content
            return StreamingResponse(io.BytesIO(audio_data), media_type="audio/mpeg")
        else:
            return self.synthesize_with_api_key(voice, req)

    def synthesize_with_api_key(self, voice, req):
        text = req["text"]
        api_key = self.get_api_key(len(text))

        response = requests.post(
            self.base_url + "/v1/text-to-speech/" + voice,
            json=req,
            headers={"xi-api-key": api_key},
        )

        if response.status_code == 200:
            audio_data = response.content
            return StreamingResponse(io.BytesIO(audio_data), media_type="audio/mpeg")
        else:
            return JSONResponse(
                content=response.json(), status_code=response.status_code
            )
