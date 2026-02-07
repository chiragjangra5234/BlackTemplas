from TTS.api import TTS
import soundfile as sf
import uuid
import os

class TextToSpeech:
    def __init__(self):
        self.tts = TTS(
            model_name="tts_models/en/vctk/vits",
            progress_bar=False,
            gpu=False
        )

    def synthesize(self, text: str) -> str:
        filename = f"audio_{uuid.uuid4().hex}.wav"
        path = os.path.join("outputs", filename)
        self.tts.tts_to_file(text=text, file_path=path)
        return path
