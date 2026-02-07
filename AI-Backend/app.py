from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import uuid
import os

from stt import SpeechToText
from tts import TextToSpeech
from intents import handle_intent
from llm import llm_response

app = FastAPI()

stt = SpeechToText()
tts = TextToSpeech()

@app.post("/voice")
async def voice_assistant(audio: UploadFile = File(...)):
    temp_audio = f"temp_{uuid.uuid4().hex}.wav"

    with open(temp_audio, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    text = stt.transcribe(temp_audio)

    intent_reply = handle_intent(text)
    if intent_reply:
        reply = intent_reply
    else:
        reply = llm_response(text)

    audio_path = tts.synthesize(reply)

    os.remove(temp_audio)

    return FileResponse(
        audio_path,
        media_type="audio/wav",
        filename="response.wav"
    )
