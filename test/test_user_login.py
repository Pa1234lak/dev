from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import TimeoutException

def test_user_login():
    BASE_URL = "https://web-app-cjv8.onrender.com"
    
    # Setup WebDriver using webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)
    
    try:
        # Step 1: Open the login page
        driver.get(f"{BASE_URL}/account/my-login")
        print("✅ Opened login page")
        
        # Step 2: Fill in the login form fields using unique IDs
        try:
            wait.until(EC.presence_of_element_located((By.ID, "id_username"))).send_keys("newuser123")
            driver.find_element(By.ID, "id_password").send_keys("Password@123")
            print("✅ Filled in login credentials")
        except TimeoutException:
            print("❌ Login form fields not found")
            return  # exit test gracefully
        
        # Step 3: Scroll into view if needed, then click the Login button
        try:
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
            driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            time.sleep(1)  # Allow any animations to finish
            login_button.click()
            print("✅ Clicked 'Login' button")
        except TimeoutException:
            print("❌ Login button not found or not clickable")
            return
        
        # Step 4: Wait for redirection to a dashboard or account page
        try:
            wait.until(EC.url_contains("/dashboard"))
            print("✅ Login successful: redirected to dashboard")
        except TimeoutException:
            print("❌ Did not redirect to dashboard after login")
        
    finally:
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    test_user_login()
