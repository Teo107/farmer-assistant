from fastapi import APIRouter

from app.services import parcels_service, report_service
from app.storage import state_store
from datetime import date

router = APIRouter()


@router.post("/generate-reports")
def generate_reports():
    """
    Simulates scheduled report sending.
    Checks which farmers are due for a report today
    and returns the messages that would be sent
    """

    res = []

    # Go through all linked phone numbers
    for phone, farmer_id in state_store.phone_to_farmer.items():

        # check if farmer should receive a report today
        if not report_service.scheduled_report(farmer_id):
            continue

        parcels = parcels_service.get_parcels_for_farmer(farmer_id)

        # if farmer has no parcels registered
        if not parcels:
            res.append({
                "to": phone,
                "message": "You currently have no registered parcels."
            })
            continue

        msg = f"You have {len(parcels)} parcels. Latest data looks stable."

        res.append({
            "to": phone,
            "message": msg
        })

        # mark report as sent
        state_store.last_report_sent[farmer_id] = str(date.today())

    return {
        "generated_at": str(date.today()),
        "reports_sent": len(res),
        "messages": res
    }
