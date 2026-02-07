import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel
import tempfile

class StreamingWhisper:
    def __init__(self):
        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    def transcribe_bytes(self, audio_bytes: bytes) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            sf.write(f.name, np.frombuffer(audio_bytes, dtype=np.int16), 16000)
            segments, _ = self.model.transcribe(f.name)
            return " ".join(seg.text for seg in segments).strip()
