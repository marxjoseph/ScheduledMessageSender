import schedule
import time
import signal
import sys
from twilio.rest import Client
from datetime import datetime
import pytz

# Twilio credentials
account_sid = "ACebc1d895587fcd3a77ca20bbc37924a7"
auth_token = "bf1981f93d8aae946c6fac6a1627c3ce"
twilio_phone_number = "+15315354346"
recipient_phone_number = "+14168337383"

# Set the timezone to Eastern Standard Time (EST)
est = pytz.timezone('US/Eastern')

# Function to send SMS
def send_sms(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=recipient_phone_number
    )
    print(f"Message sent successfully! SID: {message.sid}")

# Function to schedule SMS
def schedule_sms():
    message = "Testing the program 123"
    send_sms(message)

# Calculate the scheduled time for x EST
scheduled_datetime = est.localize(datetime.now().replace(hour=21, minute=10, second=0, microsecond=0))

# Convert the localized datetime to a string in the required format ("%H:%M")
scheduled_time_string = scheduled_datetime.strftime("%H:%M")

# Schedule the SMS to be sent at the calculated time
scheduled_job = schedule.every().day.at(scheduled_time_string).do(schedule_sms).tag('daily_sms')

# Handle Ctrl+C signal
def signal_handler(sig, frame):
    print("Received Ctrl+C. Stopping the program.")
    schedule.cancel_job(scheduled_job)
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

def main():
    print("To stop the program press CTRL+C")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
