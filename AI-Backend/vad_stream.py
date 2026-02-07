import webrtcvad
import pyaudio
import collections

class VADAudio:
    def __init__(self, rate=16000, frame_ms=30):
        self.vad = webrtcvad.Vad(2)
        self.rate = rate
        self.frame_ms = frame_ms
        self.frame_size = int(rate * frame_ms / 1000)
        self.audio = pyaudio.PyAudio()

        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            input=True,
            frames_per_buffer=self.frame_size
        )

    def listen(self):
        ring_buffer = collections.deque(maxlen=10)
        triggered = False
        voiced_frames = []

        while True:
            frame = self.stream.read(self.frame_size, exception_on_overflow=False)
            is_speech = self.vad.is_speech(frame, self.rate)

            if not triggered:
                ring_buffer.append((frame, is_speech))
                if sum(1 for _, s in ring_buffer if s) > 7:
                    triggered = True
                    voiced_frames.extend(f for f, _ in ring_buffer)
                    ring_buffer.clear()
            else:
                voiced_frames.append(frame)
                ring_buffer.append((frame, is_speech))
                if sum(1 for _, s in ring_buffer if not s) > 7:
                    yield b"".join(voiced_frames)
                    triggered = False
                    ring_buffer.clear()
                    voiced_frames = []
