from vad_stream import VADAudio
from streaming_stt import StreamingWhisper
from offline_llm import OfflineLLM
from tts import TextToSpeech
from intents import handle_intent

vad = VADAudio()
stt = StreamingWhisper()
llm = OfflineLLM()
tts = TextToSpeech()

def run():
    print("🎙️ Listening...")

    for audio_chunk in vad.listen():
        text = stt.transcribe_bytes(audio_chunk)
        if not text:
            continue

        print("User:", text)

        intent_reply = handle_intent(text)
        if intent_reply:
            reply = intent_reply
        else:
            reply = llm.chat(text)

        print("Assistant:", reply)
        audio_path = tts.synthesize(reply)

        # play locally or stream to Android
