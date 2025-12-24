import json
import os

"""
Loads farmers, parcels and parcel index monitoring data from JSON files located in the data directory 
and stores them into global in-memory variables.
This simulates a database
"""

FARMERS = []
PARCELS = []
PARCELS_INDICES = {}


def load_data():
    global FARMERS, PARCELS, PARCELS_INDICES
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    farmers_path = os.path.join(path, "farmers.json")
    parcels_path = os.path.join(path, "parcels.json")
    parcels_indices_path = os.path.join(path, "parcel_indices.json")

    with open(farmers_path, "r") as pt:
        FARMERS = json.load(pt)

    with open(parcels_path, "r") as pt:
        PARCELS = json.load(pt)

    with open(parcels_indices_path, "r") as pt:
        PARCELS_INDICES = json.load(pt)

    print("DEBUG JSON TYPE:", type(PARCELS_INDICES))
    print("DEBUG JSON SAMPLE:", str(PARCELS_INDICES)[:200])

    print("Data loaded successfully!")


