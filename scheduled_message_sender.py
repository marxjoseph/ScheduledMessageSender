import schedule
import time
import signal
import sys
import re
from twilio.rest import Client
from datetime import datetime

# Twilio credentials
account_sid = "ACebc1d895587fcd3a77ca20bbc37924a7"
auth_token = "xxx"
twilio_phone_number = "+15315354346"
recipient_phone_number = "+14168337383"

# Function to send SMS
def send_sms(message_body, times_sent, sched_once):
    for _ in range(times_sent):
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=recipient_phone_number
        )
        print(f"Message sent successfully! SID: {message.sid}")
        time.sleep(0.5)
    if(sched_once):
        print("Task Completed!")
        if(occurrence != "3"):
            schedule.cancel_job(scheduled_job)
        sys.exit(0)

# Handle signal
def signal_handler(sig, frame):
    print("Received Ctrl+C. Stopping the program.")
    if(occurrence != "3"):
        schedule.cancel_job(scheduled_job)
    sys.exit(0)

def main():
    sched_once = False
    times_sent = 1

    while(True):
        print("Would you like this message to be (Enter \"1\", \"2\", or \"3\"):")
        print("1: Occuring every day X amount of times at a sceduled time")
        print("2: Happening once X amount of times at a scheduled time")
        print("3: Occuring now X amount of times")
        global occurrence
        occurrence = input("Enter Option: ")
        if(occurrence == "1" or occurrence == "2" or occurrence == "3"):
            break
        print("That is a invalid input it must be \"1\", \"2\", or \"3\".")

    message_body = input("What would you like your message to be: ")

    # Check amount of times  to be sent
    while True:
        try:
            times_sent = int(input("How many times do you want to send the message: "))
            if times_sent > 0:
                break 
            else:
                print("Please enter a positive integer greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a positive integer greater than 0.")

    # Register the signal handler for SIGINT which is CTRL+C
    signal.signal(signal.SIGINT, signal_handler)

    if(occurrence == "3"):
        # Send the message now times_sent amount of times times then end the program
        print("To stop the program at any time press \"CTRL+C\"") 
        send_sms(message_body, times_sent, sched_once)
        print("Task Completed!")
        sys.exit(0)

    elif(occurrence == "2"):
        # Make sched_once true
        sched_once = True

    # Get scheduled time
    while True:
        message_time = input("Enter the scheduled time in military format (HH:MM, e.g., 03:25 or 16:37): ")
        # Get pattern for military time with leading zeros if needed and make sure it matches
        time_pattern = re.compile(r'^[0-2]\d:[0-5]\d$')
        if (bool(time_pattern.match(message_time))):
            break
        print("Invalid format. Please enter the time in HH:MM format with leading zeros (e.g., 03:25 or 16:37).")

    global scheduled_job
    # Schedule the SMS to be sent at the calculated time
    scheduled_job = schedule.every().day.at(message_time, "US/Eastern").do(send_sms, message_body, times_sent, sched_once)
    
    print("To stop the program at any time press \"CTRL+C\"")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
