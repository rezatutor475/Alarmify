# Alarmify
import datetime
import time
import os
import pickle
import winsound
import speech_recognition as sr
import webbrowser
import requests
from tkinter import messagebox
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class AlarmClock:
    def __init__(self):
        self.alarms = []
        self.load_alarms()  # Load previously saved alarms
        self.calendar_service = self.setup_calendar_service()  # Initialize Google Calendar service

    def set_alarm(self, datetime=None, message="", notification="popup", location="", music_file="", calendar_event=""):
        if datetime is None:
            print("Enter the alarm time (HH:MM):")
            alarm_time = input("> ")
            try:
                alarm_hour, alarm_minute = map(int, alarm_time.split(':'))
                datetime = datetime.datetime.now().replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)
            except ValueError:
                print("Invalid input. Using current time.")
                datetime = datetime.datetime.now()

        repeat_option = self.choose_repeat_option()

        repeat_days = []
        repeat_dates = []

        if repeat_option == "weekdays":
            repeat_days = ["mon", "tue", "wed", "thu", "fri"]
        elif repeat_option == "weekends":
            repeat_days = ["sat", "sun"]
        elif repeat_option == "custom":
            custom_dates = input("Enter dates to repeat (comma-separated, e.g., YYYY-MM-DD): ").strip().split(',')
            repeat_dates = [datetime.datetime.strptime(date.strip(), "%Y-%m-%d") for date in custom_dates]

        if message == "":
            message = input("Enter alarm message (optional): ").strip()

        if notification == "":
            notification = self.choose_notification_method()

        if location == "":
            location = input("Enter alarm location (optional): ").strip()

        if music_file == "":
            music_file = input("Enter path to music file for alarm sound (optional): ").strip()

        if calendar_event == "" and self.calendar_service:
            print("Syncing with Google Calendar...")
            calendar_event = self.sync_with_calendar(datetime)
            print("Calendar event synced:", calendar_event)

        alarm = Alarm(datetime, repeat_days, repeat_dates, message, notification, location, music_file, calendar_event)
        self.alarms.append(alarm)
        print("Alarm set successfully!")

    def set_alarm_voice_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for voice command...")
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print("Voice command recognized:", command)
            if 'set alarm' in command:
                current_time = datetime.datetime.now()
                if 'tomorrow' in command:
                    current_time += datetime.timedelta(days=1)
                elif 'day after tomorrow' in command:
                    current_time += datetime.timedelta(days=2)
                elif 'next week' in command:
                    current_time += datetime.timedelta(weeks=1)

                time_match = sr.findall(r'\d{1,2}:\d{2}', command)
                if time_match:
                    alarm_time = time_match[0]
                    alarm_hour, alarm_minute = map(int, alarm_time.split(':'))
                    current_time = current_time.replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)
                    self.set_alarm(datetime=current_time)
                else:
                    print("No specific time mentioned. Setting alarm for the current time.")
                    self.set_alarm()
            else:
                print("No valid voice command detected.")

        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def choose_repeat_option(self):
        print("\nChoose Repeat Option:")
        print("1. Weekdays (Monday to Friday)")
        print("2. Weekends (Saturday and Sunday)")
        print("3. Custom Days")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            return "weekdays"
        elif choice == "2":
            return "weekends"
        elif choice == "3":
            return "custom"
        else:
            print("Invalid choice. Using default (no repeat).")
            return ""

    def choose_notification_method(self):
        print("\nChoose Alarm Notification Method:")
        print("1. Popup Message")
        print("2. Sound")
        print("3. Music")
        print("4. Google Calendar Event")
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            return "popup"
        elif choice == "2":
            return "sound"
        elif choice == "3":
            return "music"
        elif choice == "4":
            return "calendar"
        else:
            print("Invalid choice. Using default (popup message).")
            return "popup"

    def display_alarms(self):
        if not self.alarms:
            print("No alarms set.")
        else:
            print("Upcoming Alarms:")
            next_alarm = self.get_next_alarm()
            if next_alarm:
                print(f"Next Alarm: {next_alarm}")
            for i, alarm in enumerate(self.alarms, start=1):
                print(f"{i}. {alarm}")

    def get_next_alarm(self):
        next_alarm = None
        for alarm in self.alarms:
            if alarm.is_upcoming():
                if not next_alarm or alarm.datetime < next_alarm.datetime:
                    next_alarm = alarm
        return next_alarm

    def delete_alarm(self):
        self.display_alarms()
        if self.alarms:
            print("Enter the alarm number to delete:")
            try:
                alarm_number = int(input("> "))
                if 1 <= alarm_number <= len(self.alarms):
                    del self.alarms[alarm_number - 1]
                    print("Alarm deleted successfully!")
                    self.save_alarms()  # Save alarms after deletion
                else:
                    print("Invalid alarm number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def snooze_alarm(self):
        self.display_alarms()
        if self.alarms:
            print("Enter the alarm number to snooze:")
            try:
                alarm_number = int(input("> "))
                if 1 <= alarm_number <= len(self.alarms):
                    alarm = self.alarms[alarm_number - 1]
                    snooze_duration = int(input("Enter snooze duration in minutes: "))
                    alarm.snooze(snooze_duration)
                    print("Alarm snoozed successfully!")
                else:
                    print("Invalid alarm number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def save_alarms(self):
        with open("alarms.pkl", "wb") as f:
            pickle.dump(self.alarms, f)
        print("Alarms saved successfully.")

    def load_alarms(self):
        if os.path.exists("alarms.pkl"):
            with open("alarms.pkl", "rb") as f:
                self.alarms = pickle.load(f)
            print("Alarms loaded successfully.")

    def setup_calendar_service(self):
        credentials = None
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json')
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', ['https://www.googleapis.com/auth/calendar.readonly']
                )
                credentials = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())

        return build('calendar', 'v3', credentials=credentials)

    def sync_with_calendar(self, datetime):
        if self.calendar_service:
            now = datetime.utcnow().isoformat() + 'Z'
            events_result = self.calendar_service.events().list(
                calendarId='primary', timeMin=now, maxResults=1, singleEvents=True,
                orderBy='startTime').execute()
            events = events_result.get('items', [])
            if events:
                event = events[0]
                start = event['start'].get('dateTime', event['start'].get('date'))
                return f"{event['summary']} - {start}"
        return ""

    def run(self):
        while True:
            print("\nAlarm Clock Menu:")
            print("1. Set Alarm")
            print("2. Display Alarms")
            print("3. Delete Alarm")
            print("4. Snooze Alarm")
            print("5. Set Alarm via Voice Command")
            print("6. Exit")
            choice = input("Enter your choice (1-6): ")

            if choice == "1":
                self.set_alarm()
            elif choice == "2":
                self.display_alarms()
            elif choice == "3":
                self.delete_alarm()
            elif choice == "4":
                self.snooze_alarm()
            elif choice == "5":
                self.set_alarm_voice_command()
            elif choice == "6":
                self.save_alarms()  # Save alarms before exiting
                break
            else:
                print("Invalid choice. Please try again.")

class Alarm:
    def __init__(self, datetime, repeat_days=[], repeat_dates=[], message="", notification="popup", location="", music_file="", calendar_event=""):
        self.datetime = datetime
        self.repeat_days = repeat_days
        self.repeat_dates = repeat_dates
        self.message = message
        self.notification = notification
        self.location = location
        self.music_file = music_file
        self.calendar_event = calendar_event
        self.is_stopped = False

    def __str__(self):
        return f"{self.datetime.strftime('%Y-%m-%d %H:%M')} {'(Repeat: ' + ', '.join(self.repeat_days) + ')' if self.repeat_days else ''} {'(Custom Dates: ' + ', '.join(date.strftime('%Y-%m-%d') for date in self.repeat_dates) + ')' if self.repeat_dates else ''} {'- ' + self.message if self.message else ''}"

    def is_upcoming(self):
        now = datetime.datetime.now()
        if self.datetime > now:
            if not self.repeat_days and not self.repeat_dates:  # No repeat set
                return True
            if not self.repeat_days or now.strftime('%a').lower() in self.repeat_days:
                return True
            if self.repeat_dates:
                return now.date() in [date.date() for date in self.repeat_dates]
        return False

    def play_music(self):
        if self.music_file and os.path.exists(self.music_file):
            winsound.PlaySound(self.music_file, winsound.SND_FILENAME)
        else:
            print("Music file not found or not provided.")

def main():
    alarm_clock = AlarmClock()
    while True:
        # Check if any alarm is due
        for alarm in alarm_clock.alarms:
            if alarm.is_upcoming():
                print(f"Alarm: {alarm.message if alarm.message else 'Wake up!'}")
                if alarm.notification == "popup":
                    messagebox.showinfo("Alarm Notification", f"{alarm.message if alarm.message else 'Wake up!'}")
                elif alarm.notification == "sound":
                    winsound.Beep(1000, 2000)  # Default beep sound
                elif alarm.notification == "music":
                    alarm.play_music()
                elif alarm.notification == "calendar":
                    print(f"Calendar Event: {alarm.calendar_event}")
                break  # Only play one alarm at a time

        time.sleep(1)  # Check every second

if __name__ == "__main__":
    main()

# Alarmify
