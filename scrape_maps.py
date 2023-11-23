from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pyperclip

# Set the path to your ChromeDriver executable
# chrome_driver_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
# options.ad
options = webdriver.ChromeOptions() 
# options.add_argument('headless') 

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com/maps/search/?api=1&query=centurylink+field")

# Find and click the "Alles afwijzen" button
try:
    button = driver.find_element(By.XPATH, '//span[text()="Alles afwijzen"]')
    button.click()
    print("Clicked on 'Alles afwijzen'")
except Exception as e:
    print(f"Error: {e}")


try:
    # Find the button by its alt attribute
        # Wait for the button by its XPath for copying the telephone number
    adres_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Adres kopiëren"]'))
    )
    # adres_button = driver.find_element(By.XPATH, '//adres_button[@aria-label="Adres kopiëren"]')
    adres_button.click()
    time.sleep(5)
    copied_address = pyperclip.paste()
    print("Copied Address:", copied_address)

    # Wait for the button by its XPath for copying the telephone number
    tel_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[6]/div[2]/div/div[1]/button'))
    )
    tel_button.click()
    time.sleep(5)
    copied_tel_number = pyperclip.paste()
    print("Copied Telephone Number:", copied_tel_number)

    # Click the button to copy the address

    # Wait for a short time to ensure the clipboard is updated

    # Retrieve the copied address from the clipboard

    # Print or use the copied address as needed


finally:
    # Close the browser window
    driver.quit()