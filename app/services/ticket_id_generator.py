from collections import defaultdict
from datetime import datetime

daily_ticket_counts = defaultdict(int)

def generate_ticket_id(phone_number):
    today = datetime.now().strftime("%m-%d-%Y")
    daily_ticket_counts[(phone_number, today)] += 1
    ticket_number = daily_ticket_counts[(phone_number, today)]
    return f"{phone_number}_{today}_ticket-{ticket_number}"
