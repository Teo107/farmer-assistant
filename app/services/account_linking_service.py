from app.storage import state_store
from app.data_loader import data_manager


def new_phone(phone: str):
    """
    Handles the first interaction for an unknown phone number
    Marks the phone as pending account linking and requests a username
    """
    if phone in state_store.pending_linking:
        return "Hello! Please provide username to link the account"

    state_store.pending_linking.add(phone)
    return "Great! Now your phone is not linked"


def try_link_account(phone: str, text: str) -> str:
    # Already linked case
    if phone in state_store.phone_to_farmer:
        farmer_id = state_store.phone_to_farmer[phone]
        return f"Your phone is already linked to farmer {farmer_id}."

    username_input = text.strip().lower()

    if not username_input:
        return ("Your phone is not linked to any account yet.\n"
                "Please type your username to link your account.")

    # Find farmer by username
    farmer = next((f for f in data_manager.FARMERS
                   if f["username"].lower() == username_input), None)

    if not farmer:
        return "Username not found."

    # CASE A: Farmer already has a phone
    if farmer["phone"]:
        if farmer["phone"] == phone:
            # Phone matches -> safe to link
            state_store.phone_to_farmer[phone] = farmer["id"]
            state_store.pending_linking.discard(phone)
            return f"Great! Your phone is now linked."
        else:
            # Someone else trying to hijack account
            return "This account is already linked to a different phone number."

    # CASE B: Farmer has no phone yet
    farmer["phone"] = phone
    state_store.phone_to_farmer[phone] = farmer["id"]
    state_store.pending_linking.discard(phone)

    return (f"Great, {farmer['name']}! Your phone is now linked.\n"
            "You can now ask about your parcels")