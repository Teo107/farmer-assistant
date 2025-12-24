import os
import json
from google import genai
from dotenv import load_dotenv


# Load API key from .env
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "models/gemini-2.5-flash"

# force the AI to behave like a intent classifier
SYSTEM_PROMPT = """
You are an intent classifier for a farmer assistant chatbot.

You MUST ALWAYS return valid JSON only.
Never include explanations or markdown.

JSON schema:
{
  "intent": "GREETING | LIST_PARCELS | PARCEL_DETAILS | PARCEL_STATUS | SET_REPORT_FREQUENCY | STOP_REPORTS | UNKNOWN",
  "parcel_id": "P1 | P2 | null",
  "frequency": "daily | weekly | monthly | null"
}

Rules:
- Greeting → GREETING only if the message contains a greeting
- "show my parcels" → LIST_PARCELS
- "show P3 / details P3" → PARCEL_DETAILS
    If message contains "parcel Px" or "P<number>" → PARCEL_DETAILS. Extract parcel_id even if intent is UNKNOWN
- "how is P3 / status / summary" → PARCEL_STATUS
- contains 'daily/weekly/monthly' → SET_REPORT_FREQUENCY
- contains 'stop / disable' → STOP_REPORTS
- otherwise UNKNOWN
Always choose a valid intent.
Return ONLY JSON.
"""


def parse_message(text: str) -> str:
    """
    Sends the user text to Gemini and returns raw JSON intent result
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=f"{SYSTEM_PROMPT}\nUser: \"{text}\"",
        config={"response_mime_type": "application/json"}
    )

    raw = response.text.strip()

    raw = raw.replace("```json", "").replace("```", "").strip()
    return raw


def call_ai(prompt: str) -> str:
    """
    Used when we want gemini to generate a friendly human-like message
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text.strip()
