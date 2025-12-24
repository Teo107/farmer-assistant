from app.services.ai_service import call_ai


def ai_format_response(intent_result):
    """
    Formats chatbot responses when AI mode is enabled
    For simple deterministic cases (greeting / unknown) it returns fixed text
    For anything else, it delegates message phrasing to the AI
    """
    t = intent_result.get("type")

    if t == "GREETING":
        return (
            "Welcome to the CO2 Angels Farm Assistant!\n"
            "You can ask me things like:\n"
            "• Show my parcels\n"
            "• Show parcel P2 details\n"
            "• How is parcel P1 doing?\n"
            "• Set weekly reports\n"
            "• Stop reports"
        )

    if t == "UNKNOWN":
        return (
            "Sorry, I’m not sure what you mean.\n"
            "Try something like:\n"
            "- Show parcels\n"
            "- Parcel P3 details\n"
            "- Set daily reports"
        )

    prompt = f"""You are a helpful agricultural assistant. You will receive structured JSON data.
    Generate a friendly message for the farmer. Be short, clear, and human.
    DATA: {intent_result}"""
    return call_ai(prompt)
