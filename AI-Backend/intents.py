def handle_intent(text: str):
    text = text.lower()

    if "pension" in text:
        return "Your pension has been credited successfully."

    if "open document" in text:
        return "Opening your document now."

    if "emergency" in text:
        return "Calling your emergency contact."

    return None  # Send to LLM