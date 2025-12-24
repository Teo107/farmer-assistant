from app.services import parcels_service
from app.services.parcel_summary_service import build_parcel_summary
from app.storage import state_store

def handle_intent(intent_obj, farmer_id, phone):
    """
    Handles the AI-parsed intent
    Based on the classified intent, this function routes the request to the correct backend logic
    """

    intent = intent_obj.get("intent")
    parcel_id = intent_obj.get("parcel_id")
    frequency = intent_obj.get("frequency")

    if intent == "GREETING":
        return {"type": "GREETING"}

    if intent == "LIST_PARCELS":
        parcels = parcels_service.get_parcels_for_farmer(farmer_id)
        return {"type": "LIST_PARCELS", "parcels": parcels}

    if intent == "PARCEL_DETAILS":
        details, error = parcels_service.parcel_details_for_farmer(farmer_id, parcel_id)
        return {"type": "PARCEL_DETAILS", "error": error, "data": details}

    if intent == "PARCEL_STATUS":
        summary, error = build_parcel_summary(parcel_id)
        return {"type": "PARCEL_STATUS", "error": error, "data": summary}

    if intent == "SET_REPORT_FREQUENCY":
        state_store.report_freq[farmer_id] = frequency
        return {"type": "SET_REPORT_FREQUENCY", "frequency": frequency}

    if intent == "STOP_REPORTS":
        state_store.report_freq.pop(farmer_id, None)
        return {"type": "STOP_REPORTS"}

    return {"type": "UNKNOWN"}