from datetime import datetime
from app.services.parcels_service import get_latest_indices, get_parcel_by_id


# Normalized Difference Vegetation Index
def classify_ndvi(v):
    if v is None:
        return "No vegetation data available."
    if v < 0.3:
        return f"NDVI is {v}, indicating poor vegetation."
    if 0.3 <= v < 0.55:
        return f"NDVI is {v}, indicating moderate vegetation."
    if 0.55 <= v < 0.75:
        return f"NDVI is {v}, indicating good vegetation"

    return f"NDVI is {v}, indicating strong vegetation."


# Moisture Index
def classify_ndmi(v):
    if v is None:
        return "No moisture data available."
    if v < 0.15:
        return f"NDMI is {v}, indicating dry moisture"
    if 0.15 <= v < 0.30:
        return f"NDMI is {v}, indicating average moisture"

    return "NDMI is {v}, indicating good moisture"


# Water Index
def classify_ndwi(v):
    if v is None:
        return "No water data available."
    if v < 0.10:
        return f"Water index (NDWI) is low ({v})."
    if 0.10 <= v < 0.25:
        return f"Water index (NDWI) is average ({v})."
    return f"Water index (NDWI) is good ({v})"


# Soil Organic Carbon
def classify_soc(v):
    if v is None:
        return "No soil organic carbon data available."
    if v < 1.5:
        return f"SOC is {v}, indicating poor soil organic matter"
    if 1.5 <= v < 2.5:
        return f"SOC is {v}, indicating moderate oil organic matter"

    return "SOC is {v}, indicating rich organic content"


# Nitrogen
def classify_N(v):
    if v is None:
        return "No nitrogen data available."
    if v < 0.7:
        return f"Nitrogen is {v}, indicating crop may need nitrogen fertilization"
    if 0.7 <= v < 1.0:
        return f"Nitrogen is {v}, indicating crop has adequate nitrogen fertilization"

    return "Nitrogen is {v}, indicating high nitrogen fertilization"


# Phosphorus
def classify_P(v):
    if v is None:
        return "No phosphorus data available."
    if v < 0.35:
        return f"Phosphorus is {v}, indicating crop may need phosphorus fertilization"
    if 0.35 <= v < 0.45:
        return f"Phosphorus is {v}, indicating crop has adequate phosphorus fertilization"

    return "Phosphorus is {v}, indicating high phosphorus fertilization"


# Potassium
def classify_K(v):
    if v is None:
        return "No potassium data available."
    if v < 0.55:
        return f"Potassium is {v}, indicating crop may need potassium fertilization"
    if 0.55 <= v < 0.7:
        return f"Potassium is {v}, indicating crop has adequate potassium fertilization"

    return "Potassium is {v}, indicating high/good phosphor fertilization"


# pH Level
def classify_ph(v):
    if v is None:
        return "No pH data available."
    if v < 5.5:
        return f"pH is {v}, indicating strongly acidic soil."
    if 5.5 <= v < 6.0:
        return f"pH is {v}, indicating slightly acidic"
    if 6.0 <= v < 7.0:
        return f"pH is {v}, near optimal. This is good for most crops"

    return f"pH is {v},slightly alkalin"


def build_parcel_summary(parcel_id:str):
    parcel = get_parcel_by_id(parcel_id)
    if parcel is None:
        return None, "Parcel not found"

    latest = get_latest_indices(parcel_id)
    if not latest:
        return None, "No monitoring data available for this parcel"

    ndvi = latest.get("ndvi")
    ndmi = latest.get("ndmi")
    ndwi = latest.get("ndwi")
    soc = latest.get("soc")
    n = latest.get("nitrogen")
    p = latest.get("phosphorus")
    k = latest.get("potassium")
    ph = latest.get("ph")
    date = latest.get("date")

    ndvi_text = classify_ndvi(ndvi)
    ndmi_text = classify_ndmi(ndmi)
    ndwi_text = classify_ndwi(ndwi)
    soc_text = classify_soc(soc)
    n_text = classify_N(n)
    p_text = classify_P(p)
    k_text = classify_K(k)
    ph_text = classify_ph(ph)

    reply = (
        f"Parcel {parcel_id} – {parcel['name']}\n"
        f"Status update based on latest data ({date}):\n\n"
        f"Vegetation:\n"
        f"    - {ndvi_text}\n\n"

        f"Moisture & Water:\n"
        f"    - {ndmi_text}\n"
        f"    - {ndwi_text}\n\n"

        f"Soil Quality:\n"
        f"    - {soc_text}\n\n"

        f"Nutrients:\n"
        f"    - {n_text}\n"
        f"    - {p_text}\n"
        f"    - {k_text}\n\n"

        f"Soil pH:\n"
        f"    - {ph_text}"
    )

    return {"reply": reply}, None


