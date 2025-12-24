import json

from fastapi import APIRouter

from app.services.ai_handler import handle_intent
from app.storage import state_store
from app.services import account_linking_service, parcels_service, ai_service
from pydantic import BaseModel, Field
from app.services.parcel_summary_service import build_parcel_summary

# from app.services import ai_service
# from app.services.ai_handler import handle_intent

"""
message_router.py
Main conversational entrypoint. Receives messages from frontend and routes
them to account linking, parcel lookup, summary generation, and reporting logic.

AI MODE:
 if USE_AI = True → AI interprets user intent and generates natural language reply
- business logic and data retrieval are still validated in backend
"""

USE_AI = False
router = APIRouter()


class MessagePayload(BaseModel):
    from_: str = Field(alias="from", example="+40740000000")
    text: str = Field(example="hello")

    model_config = {
        "validate_by_name": True
    }


@router.post("/message")
def handle_message(payload: MessagePayload):
    """
    Main chatbot message handler.
    Decides whether the user is linking account, requesting parcel list,
    asking parcel details, requesting a status summary or setting report frequency.
    Returns structured JSON response
    """

    phone = payload.from_
    text = payload.text.strip()

    # account linked
    if phone in state_store.phone_to_farmer:
        # identify farmer
        # every request is associated with exactly one farmer
        # a farmer cannot see another farmer s parcels
        farmer_id = state_store.phone_to_farmer[phone]

        # Greeting logic
        # We only treat the message as a greeting if it ONLY contains greeting text. Ex:
        # "hello" -> greeting
        # "hello show parcels" -> not greeting
        text_lower = text.lower()
        greetings = ["hello", "hi", "hey", "salut", "good morning", "good evening"]

        if any(g in text_lower for g in greetings) and len(text_lower.split()) <= 2:
            return {
                "reply":
                    "Welcome to the CO2 Angels Farm Assistant!\n"
                    "You can ask me things like:\n"
                    "- Show my parcels\n"
                    "- Show parcel P2 details\n"
                    "- How is parcel P1 doing?\n"
                    "- Set weekly reports\n"
                    "- Stop reports"
            }

        """
        AI:
        - AI parses user intent (list parcels, summary, details, etc.)
        - Backend still fetches real data and validates security
        - AI only formats final text response in natural language
        - if AI fails → automatic fallback to deterministic rule logic
        """
        if USE_AI:
            try:
                intent_raw = ai_service.parse_message(text)
                intent = json.loads(intent_raw)

                result = handle_intent(intent, farmer_id, phone)

                from app.services.ai_response import ai_format_response
                reply = ai_format_response(result)
                reply = reply.replace("\n", "\r\n")
                return {"reply": reply, "raw": result}

            except Exception as e:
                print("AI failed, falling back:", e)

        # report logic
        # Stored per farmer, not per phone, because a farmer may have multiple devices
        text_lower = text.lower()
        if "daily" in text_lower:
            state_store.report_freq[farmer_id] = "daily"
            return {"reply": "Okay! I’ve set your report frequency to daily."}

        if "weekly" in text_lower:
            state_store.report_freq[farmer_id] = "weekly"
            return {
                "reply": "Got it! I’ll prepare a parcel summary for you every week based on your latest available data."}

        if "monthly" in text_lower:
            state_store.report_freq[farmer_id] = "monthly"
            return {"reply": "OK! I’ve set your report frequency to monthly."}

        if "stop" in text_lower or "disable" in text_lower:
            if farmer_id not in state_store.report_freq:
                return {"reply": "You don't have any report schedule set."}

            state_store.report_freq.pop(farmer_id, None)
            return {"reply": "Reports disabled successfully."}

        # parcel status with all info
        parcel_id = parcels_service.extract_parcel_id(text)
        if parcel_id:
            words = text_lower.split()
            if any(word in words for word in ["how", "status", "summary"]):
                parcel, err = parcels_service.parcel_details_for_farmer(farmer_id, parcel_id)
                if err:
                    return {"reply": err}

                summary, error = build_parcel_summary(parcel_id)
                if error:
                    return {"reply": error}
                return summary

            # Normal parcel details
            details, error = parcels_service.parcel_details_for_farmer(farmer_id, parcel_id)
            if error:
                return {"reply": error}

            latest = details.get("latest indices")

            reply = (
                f"Parcel {details['id']} – {details['name']}\n"
                f"Crop: {details['crop']}\n"
                f"Area: {details['area_ha']} ha\n"
                f"Latest data: {latest['date']}:\n"
                f"     NDVI: {latest['ndvi']}\n"
                f"     NDMI: {latest['ndmi']}\n"
                f"     NDWI: {latest['ndwi']}\n"
                f"     SOC: {latest['soc']}\n"
                f"     N: {latest['nitrogen']}\n"
                f"     P: {latest['phosphorus']}\n"
                f"     K: {latest['potassium']}\n"
                f"     pH: {latest['ph']}"
            )

            return {"reply": reply}

        # list parcels
        if "parcel" in text_lower or "parcels" in text_lower or "field" in text_lower or "fields" in text_lower:
            parcels = parcels_service.get_parcels_for_farmer(farmer_id)

            if not parcels:
                return {"reply": "You don’t have any parcels registered yet."}

            reply_lines = [f"You have {len(parcels)} parcels:"]
            for p in parcels:
                reply_lines.append(f"{p['id']} – {p['name']} ({p['area_ha']} ha, {p['crop']})")

            reply = "\n".join(reply_lines)

            return {"reply": reply}

        # if message does not match any supported command it returns guided help list
        return {
            "reply":
                "I didn’t fully understand tha \n"
                "Try one of these:\n"
                "- Show my parcels\n"
                "- Show parcel P3\n"
                "- How is P1 doing?\n"
                "- Set daily reports"
        }

    # link account
    # if user is not linked yet, try to link account using the text as username
    reply = account_linking_service.try_link_account(phone, text)
    if reply != "Username not found":
        return {"reply": reply}

    # if phone number is seen for the first time, mark it as "pending linking" and ask user for username
    if phone not in state_store.pending_linking:
        reply = account_linking_service.new_phone(phone)
        return {"reply": reply}

    # otherwise user is already in linking flow but sent an invalid username
    return {"reply": "Username not found"}


@router.get("/debug/state")
def debug_state():
    """
    Debug endpoint to inspect in-memory chatbot state
    """

    return {
        "phone_to_farmer": state_store.phone_to_farmer,
        "pending_linking": list(state_store.pending_linking),
        "report_freq": state_store.report_freq
    }
