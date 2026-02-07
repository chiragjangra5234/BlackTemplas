from llama_cpp import Llama

class OfflineLLM:
    def __init__(self):
        self.llm = Llama(
            model_path="models/llm/llama-2-7b-chat.gguf",
            n_ctx=2048,
            n_threads=6
        )

    def chat(self, text: str) -> str:
        prompt = f"""
You are a calm, polite assistant for elderly people.
Use very simple words.
Answer briefly.

User: {text}
Assistant:
"""
        output = self.llm(prompt, max_tokens=150, stop=["User:"])
        return output["choices"][0]["text"].strip()
