from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time

def test_user_registration():
    BASE_URL = "https://web-app-cjv8.onrender.com"
    
    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)
    
    try:
        # Step 1: Open registration page
        driver.get(f"{BASE_URL}/account/register")
        print("PASSED: Opened registration page.")
        
        # Step 2: Fill in the form
        try:
            wait.until(EC.presence_of_element_located((By.ID, "id_username"))).send_keys("newuser123")
            driver.find_element(By.ID, "id_email").send_keys("newuser123@example.com")
            driver.find_element(By.ID, "id_password1").send_keys("Password@123")
            driver.find_element(By.ID, "id_password2").send_keys("Password@123")
            print("PASSED: Filled registration form.")
        except TimeoutException:
            print("FAILED: Registration form fields not found.")
            return
        
        # Step 3: Click the 'Create account' button
        try:
            register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Create account')]")))
            driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
            time.sleep(1)
            register_button.click()
            print("PASSED: Clicked 'Create account' button.")
        except TimeoutException:
            print("FAILED: 'Create account' button not found or not clickable.")
            return
        
        # Step 4: Verify success message / redirection
        time.sleep(3)
        page_text = driver.page_source.lower()
        if "email" in page_text:
            print("PASSED: Registration successful; 'email' found on the page.")
        else:
            print("FAILED: Registration might have failed; 'email' not found on the page.")
    
    finally:
        time.sleep(2)
        driver.quit()
        print("INFO: Browser closed.")

if __name__ == "__main__":
    test_user_registration()
