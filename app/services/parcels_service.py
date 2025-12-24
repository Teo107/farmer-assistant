import re
from app.data_loader import data_manager


def get_parcels_for_farmer(farmer_id: str):
    """
    Returns all parcels belonging to a given farmer
    """
    res = []
    for parcel in data_manager.PARCELS:
        if parcel["farmer_id"] == farmer_id:
            res.append(parcel)
    return res


def get_latest_indices(parcel_id: str):
    """
    Retrieves the latest monitoring index record for a given parcel (the newest)
    """
    if parcel_id not in data_manager.PARCELS_INDICES:
        return None

    records = data_manager.PARCELS_INDICES[parcel_id]
    if not records:
        return None

    sorted_records = sorted(records, key=lambda r: r["date"], reverse=True)
    return sorted_records[0]


def parcel_details_for_farmer(farmer_id: str, parcel_id: str):
    """
    Returns details for a specific parcel only if it belongs to the given farmer.
    """
    parcel = get_parcel_by_id(parcel_id)
    if parcel is None:
        return None, "Parcel not found"
    if parcel["farmer_id"] != farmer_id:
        return None, "This parcel does not belong to you.."

    latest = get_latest_indices(parcel_id)
    return {
        "id": parcel["id"],
        "name": parcel["name"],
        "area_ha": parcel["area_ha"],
        "crop": parcel["crop"],
        "latest indices": latest
    }, None


def get_parcel_by_id(parcel_id: str):
    """
    Finds and returns a parcel object by parcel ID
    """
    for p in data_manager.PARCELS:
        if p["id"] == parcel_id:
            return p
    return None


def extract_parcel_id(text: str) -> str | None:
    """
    Finds in the text if it is about a parcel (PX)
    """
    text_upper = text.upper()
    matches = re.findall(r"P\s*\d+", text_upper)
    if not matches:
        return None
    return matches[0].replace(" ", "")
