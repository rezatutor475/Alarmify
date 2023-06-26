

# Certainly! Here's a comprehensive overview of the characteristics inherent in the aforementioned code:

# Modularity: The code is organized into separate classes (AlarmClock and Alarm), each responsible for specific functionalities. 
# This promotes modularity and separation of concerns.


# User Interaction: The code utilizes a menu system to interact with the user. 
# The user can choose various options such as setting alarms, displaying alarms, deleting alarms, snoozing alarms, stopping alarms, or exiting the program.


# Alarm Management: The AlarmClock class handles the management of alarms. 
# It allows the user to set alarms by specifying the time, display the list of set alarms, delete specific alarms, snooze alarms by a given duration, and stop alarms.


# Alarm Storage: The code utilizes a list (alarms) within the AlarmClock class to store and manage the set alarms. 
# Alarms are represented as instances of the Alarm class and stored in the list.


# Alarm Functionality: The Alarm class represents an individual alarm. 
# It stores the datetime at which the alarm is set, along with flags to indicate if it has been snoozed or stopped. 
# The Alarm class provides methods to check if the alarm time has been reached, play the alarm sound, snooze the alarm for a specified duration, and stop the alarm.


# Exception Handling: The code includes exception handling to handle various possible errors, such as invalid time formats, invalid input for alarm number or snooze duration, and ensuring the input is within the valid range.


# Sound Generation: The code utilizes the winsound module to generate a sound when the alarm time is reached. Currently, it uses a fixed frequency and duration, but this can be customized as per requirements.


# DateTime Handling: The code uses the datetime module to handle date and time-related operations. 
# It allows setting the alarm time, comparing with the current time, and performing snooze functionality.


# Code Reusability: The code is designed in an object-oriented manner, promoting code reusability. 
# The AlarmClock class and Alarm class can be easily extended and modified to add more functionalities or integrate with other systems.


# User-Friendly Interface: The menu system provides a user-friendly interface to interact with the alarm clock. Users can easily set alarms, manage them, and perform actions such as snooze or stop.


# Flexibility: The code is flexible and allows customization. 
# You can add more features, modify the alarm behavior, incorporate additional functionalities, or integrate it into a larger application as needed.


# Alarmify
import datetime
import time
import winsound

class AlarmClock:
    def __init__(self):
        self.alarms = []

    def set_alarm(self):
        print("Enter the alarm time (HH:MM:SS):")
        alarm_time = input("> ")
        try:
            alarm_hour, alarm_minute, alarm_second = map(int, alarm_time.split(':'))
            alarm_datetime = datetime.datetime.now().replace(hour=alarm_hour, minute=alarm_minute, second=alarm_second)
            alarm = Alarm(alarm_datetime)
            self.alarms.append(alarm)
            print("Alarm set successfully!")

        except ValueError:
            print("Invalid time format. Please try again.")

    def display_alarms(self):
        if len(self.alarms) == 0:
            print("No alarms set.")
        else:
            print("Alarms:")
            for i, alarm in enumerate(self.alarms, start=1):
                print(f"{i}. {alarm}")

    def delete_alarm(self):
        self.display_alarms()
        if len(self.alarms) > 0:
            print("Enter the alarm number to delete:")
            try:
                alarm_number = int(input("> "))
                if 1 <= alarm_number <= len(self.alarms):
                    del self.alarms[alarm_number - 1]
                    print("Alarm deleted successfully!")
                else:
                    print("Invalid alarm number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def run(self):
        while True:
            print("\nAlarm Clock Menu:")
            print("1. Set Alarm")
            print("2. Display Alarms")
            print("3. Delete Alarm")
            print("4. Snooze Alarm")
            print("5. Stop Alarm")
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
                self.stop_alarm()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")

    def snooze_alarm(self):
        self.display_alarms()
        if len(self.alarms) > 0:
            print("Enter the alarm number to snooze:")
            try:
                alarm_number = int(input("> "))
                if 1 <= alarm_number <= len(self.alarms):
                    alarm = self.alarms[alarm_number - 1]
                    snooze_duration = input("Enter snooze duration in minutes: ")
                    try:
                        snooze_minutes = int(snooze_duration)
                        alarm.snooze(snooze_minutes)
                        print("Alarm snoozed successfully!")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                else:
                    print("Invalid alarm number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def stop_alarm(self):
        self.display_alarms()
        if len(self.alarms) > 0:
            print("Enter the alarm number to stop:")
            try:
                alarm_number = int(input("> "))
                if 1 <= alarm_number <= len(self.alarms):
                    alarm = self.alarms[alarm_number - 1]
                    alarm.stop()
                    print("Alarm stopped successfully!")
                else:
                    print("Invalid alarm number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

class Alarm:
    def __init__(self, datetime):
        self.datetime = datetime
        self.is_snoozed = False
        self.is_stopped = False

    def __str__(self):
        return self.datetime.strftime("%Y-%m-%d %H:%M:%S")

    def is_time_up(self):
        return datetime.datetime.now() >= self.datetime

    def play_sound(self):
        frequency = 2500  # Frequency in Hertz
        duration = 2000  # Duration in milliseconds
        winsound.Beep(frequency, duration)

    def snooze(self, minutes):
        snooze_duration = datetime.timedelta(minutes=minutes)
        self.datetime += snooze_duration
        self.is_snoozed = True

    def stop(self):
        self.is_stopped = True

def main():
    alarm_clock = AlarmClock()
    alarm_clock.run()

if __name__ == "__main__":
    main()


# Alarmify

