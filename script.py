# script.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time

# URL of the website to check
url = 'https://www.fe.um.si/aktualna-obvestila.html?...'  # Replace with your actual URL

def check_new_notifications():
    try:
        # Set up headless Chrome options
        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Initialize the WebDriver
        driver = webdriver.Chrome(options=options)

        # Open the webpage
        driver.get(url)

        # Wait for the page to load completely
        time.sleep(5)  # You can adjust this sleep time as needed

        # Find the element by ID
        badge_element = driver.find_element(By.ID, 'cp_total_results')

        if badge_element and badge_element.text.strip():
            current_notifications = int(badge_element.text.strip())
            print(f"Current number of notifications: {current_notifications}")
        else:
            print("Could not find the number of notifications.")
            return

        # Check if the count has increased
        if os.path.exists('stevilo_obvestil.txt'):
            with open('stevilo_obvestil.txt', 'r') as f:
                previous_notifications = int(f.read().strip())
        else:
            previous_notifications = 0

        if current_notifications > previous_notifications:
            print("New notifications detected! Sending email...")
            send_email(current_notifications)
        else:
            print("No new notifications.")

        # Update the notification count
        with open('stevilo_obvestil.txt', 'w') as f:
            f.write(str(current_notifications))

        # Close the browser
        driver.quit()

    except Exception as e:
        print(f"Error checking notifications: {e}")

def send_email(notification_count):
    try:
        # List of recipients
        recipients = ['grega.grajzl@student.um.si']  # Add more recipients as needed

        url = 'https://formspree.io/f/manwrpzz'  # Your Formspree URL
        mail_body = f"New notification!\nThere is a new notification on the website.\n\n"
        mail_body += f"View notifications: {url}"  # Add the actual URL

        for recipient in recipients:
            data = {
                'email': recipient,
                'message': mail_body
            }
            response = requests.post(url, data=data)

            if response.status_code == 200:
                print(f"Email successfully sent to {recipient}!")
            else:
                print(f"Error sending email to {recipient}: {response.status_code}")

    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    check_new_notifications()
