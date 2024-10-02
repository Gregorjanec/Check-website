import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# ... (other imports)

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
        # ... (rest of your code)
    except Exception as e:
        print(f"Error checking notifications: {e}")
    finally:
        driver.quit()
