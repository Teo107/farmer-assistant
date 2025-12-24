"""
Temporary data stored in memory while the app runs
Used for account linking and scheduled reporting preferences
"""
phone_to_farmer = {}
pending_linking = set()

report_freq = {} # daily, weekly or monthly
last_report_sent = {}

