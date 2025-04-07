from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_order_total_display():
    BASE_URL = "https://web-app-cjv8.onrender.com"

    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)

    try:
        # Step 1: Go to the cart page
        driver.get(f"{BASE_URL}/cart")
        print("PASSED: Opened cart page.")

        # Step 2: Look for the total element
        try:
            total_element = wait.until(EC.presence_of_element_located((By.ID, "total")))
            total_value = total_element.text.strip()

            if total_value:
                print(f"PASSED: Found total element with value: {total_value}")
            else:
                print("FAILED: 'total' element is present but empty.")
        except TimeoutException:
            print("FAILED: 'total' element not found on the cart page.")

    finally:
        time.sleep(2)
        driver.quit()
        print("INFO: Browser closed.")

if __name__ == "__main__":
    test_order_total_display()
