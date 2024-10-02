import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

# URL of the website to check
url = 'https://www.fe.um.si/aktualna-obvestila.html?option=com_customproperties&view=search&Itemid=427&lang=sl&cp%5Bprogram%5D%5B%5D=mag&cp%5Bletnik%5D%5B%5D=1_letnik&cp%5Bnacin%5D%5B%5D=redni&cp%5Blokacija%5D%5B%5D=krsko&submit_search='

def check_new_notifications():
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Use webdriver-manager to handle ChromeDriver installation
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)

        # Wait for the element to load
        wait = WebDriverWait(driver, 10)
        badge_element = wait.until(EC.presence_of_element_located((By.ID, 'cp_total_results')))

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

    except Exception as e:
        print(f"Error checking notifications: {e}")

    finally:
        driver.quit()

def send_email(notification_count):
    try:
        # List of recipients
        recipients = ['grega.grajzl@student.um.si']  # Add more recipients as needed

        formspree_url = 'https://formspree.io/f/manwrpzz'  # Your Formspree URL
        mail_body = f"Novo obvestilo!\nNa spletni strani je bilo objavljeno novo obvestilo.\n\n"
        mail_body += f"Ogled obvestil: {url}"

        for recipient in recipients:
            data = {
                'email': recipient,
                'message': mail_body
            }
            response = requests.post(formspree_url, data=data)

            if response.status_code == 200 or response.status_code == 201:
                print(f"E-pošta uspešno poslana prejemniku {recipient}!")
            else:
                print(f"Napaka pri pošiljanju e-pošte prejemniku {recipient}: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Napaka pri pošiljanju e-pošte: {e}")

if __name__ == "__main__":
    check_new_notifications()
