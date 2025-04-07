from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
        print("✅ Opened login page")

        try:
            wait.until(EC.presence_of_element_located((By.ID, "id_username"))).send_keys("newuser123")
            driver.find_element(By.ID, "id_password").send_keys("Password@123")
            print("✅ Entered login credentials")
        except TimeoutException:
            print("❌ Login input fields not found")
            return

        try:
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
            driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            time.sleep(1)
            login_button.click()
            print("✅ Clicked 'Login' button")
        except TimeoutException:
            print("❌ Login button not found or not clickable")
            return

        # Step 2: Wait for dashboard page to load
        try:
            wait.until(EC.url_contains("/dashboard"))
            print("✅ Logged in and redirected to dashboard")
        except TimeoutException:
            print("❌ Login failed or dashboard not loaded")
            return

        # Step 3: Click "Track Order" link/button
        try:
            track_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Track Order")))
            track_link.click()
            print("✅ Clicked 'Track Order' link")
        except TimeoutException:
            print("❌ 'Track Order' link not found or not clickable")
            return

        # Step 4: Check for "order status" on the tracking page
        time.sleep(2)
        if "order status" in driver.page_source.lower():
            print("✅ Order tracking page loaded with 'order status'")
        else:
            print("❌ 'order status' not found on the tracking page")

    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    test_order_tracking_dashboard()
