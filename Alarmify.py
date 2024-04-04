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
