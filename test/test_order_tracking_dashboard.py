from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_order_tracking_dashboard():
    BASE_URL = "https://web-app-cjv8.onrender.com"
    
    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)

    try:
        # Step 1: Login first
        driver.get(f"{BASE_URL}/account/my-login")
        print("PASSED: Opened login page.")

        try:
            wait.until(EC.presence_of_element_located((By.ID, "id_username"))).send_keys("PALAKJETHWANI")
            driver.find_element(By.ID, "id_password").send_keys("123Palak456#")
            print("PASSED: Entered login credentials.")
        except TimeoutException:
            print("FAILED: Login input fields not found.")
            return

        try:
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
            driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            time.sleep(1)
            login_button.click()
            print("PASSED: Clicked 'Login' button.")
        except TimeoutException:
            print("FAILED: Login button not found or not clickable.")
            return

        # Step 2: Wait for dashboard page to load
        try:
            wait.until(EC.url_contains("/dashboard"))
            print("PASSED: Logged in and redirected to dashboard.")
        except TimeoutException:
            print("FAILED: Login failed or dashboard not loaded.")
            return

        # Step 3: Click "My orders" button
        try:
            my_orders_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "My orders")))
            my_orders_btn.click()
            print("PASSED: Clicked 'My orders' button.")
        except TimeoutException:
            print("FAILED: 'My orders' button not found or not clickable.")
            return

    finally:
        time.sleep(2)
        driver.quit()
        print("INFO: Browser closed.")

if __name__ == "__main__":
    test_order_tracking_dashboard()
