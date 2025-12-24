from datetime import date, timedelta
from app.storage import state_store

def scheduled_report(farmer_id: str) -> bool:
    """
    Determines whether a scheduled report should be sent to a farmer, based on their configured reporting
    frequency and the last time a report was sent
    """
    freq = state_store.report_freq.get(farmer_id)
    if not freq:
        return False

    today = date.today()
    last = state_store.last_report_sent.get(farmer_id)

    if freq == "daily":
        return last != str(today)

    if freq == "weekly":
        if not last:
            return True
        last_date = date.fromisoformat(last)
        return (today - last_date).days >=7

    if freq == "monthly":
        if not last:
            return True
        last_date = date.fromisoformat(last)
        return (today.year != last_date.year) or (today.month != last_date.month)
      # return (today - last_date).days >= 30  # -> to sand at each 30 days
    return False