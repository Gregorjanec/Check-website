import requests
from bs4 import BeautifulSoup
import os

url = 'https://www.fe.um.si/aktualna-obvestila.html?...'  # Your URL

def check_new_notifications():
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        badge_element = soup.find('span', id='cp_total_results')

        if badge_element and badge_element.text.strip():
            current_notifications = int(badge_element.text.strip())
            print(f"Current number of notifications: {current_notifications}")
        else:
            print("Could not find the number of notifications.")
            return

        if os.path.exists('stevilo_obvestil.txt'):
            with open('stevilo_obvestil.txt', 'r') as f:
                previous_notifications = int(f.read().strip())
        else:
            previous_notifications = 0

        if current_notifications > previous_notifications:
            print("New notifications detected! Sending email...")
            send_email(current_notifications)

        # Update the notification count
        with open('stevilo_obvestil.txt', 'w') as f:
            f.write(str(current_notifications))

    except Exception as e:
        print(f"Error checking notifications: {e}")

def send_email(notification_count):
    # Your email sending logic using Formspree
    pass

if __name__ == "__main__":
    check_new_notifications()
