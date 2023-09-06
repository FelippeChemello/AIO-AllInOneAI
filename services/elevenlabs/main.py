from fastapi import APIRouter

from services.elevenlabs.Elevenlabs import ElevenLabsTTS

router = APIRouter()

elevenlabs_tts = ElevenLabsTTS()


@router.get("/v1/voices")
def get_voices():
    return elevenlabs_tts.get_voices()


@router.post("/v1/text-to-speech/{voice}")
def synthesize(voice: str, req: dict):
    return elevenlabs_tts.synthesize(voice, req)


@router.get("/v1/usage")
def get_usage():
    return elevenlabs_tts.get_all_usage()
