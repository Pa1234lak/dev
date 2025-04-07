from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_shipping_and_paypal_button():
    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Go to the checkout page
        driver.get("https://web-app-cjv8.onrender.com/payment/checkout")
        print("PASSED: Opened checkout page.")

        # Step 2: Fill in the form
        try:
            wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Test User")
            driver.find_element(By.ID, "email").send_keys("test@example.com")
            driver.find_element(By.ID, "address1").send_keys("123 Test Street")
            # Skipping second 'address1' to avoid duplicate entry
            driver.find_element(By.ID, "city").send_keys("Testville")
            driver.find_element(By.ID, "state").send_keys("CA")
            driver.find_element(By.ID, "zipcode").send_keys("12345")
            print("PASSED: Form fields filled.")
        except NoSuchElementException as e:
            print(f"FAILED: Form element not found: {e}")
            return

        # Wait for JS to process (and PayPal button to render)
        time.sleep(3)

        # Step 3: Switch into PayPal iframe
        try:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            paypal_frame = None
            for iframe in iframes:
                src = iframe.get_attribute("src")
                if src and "paypal" in src.lower():
                    paypal_frame = iframe
                    break

            if not paypal_frame:
                print("FAILED: PayPal iframe not found.")
                return

            driver.switch_to.frame(paypal_frame)
            print("PASSED: Switched to PayPal iframe.")
        except Exception as e:
            print(f"FAILED: Error switching to iframe: {e}")
            return

        # Step 4: Check for PayPal button
        try:
            paypal_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button")))
            if paypal_btn.is_enabled():
                print("SUCCESS: PayPal button is enabled.")
            else:
                print("FAILED: PayPal button is present but disabled.")
        except TimeoutException:
            print("FAILED: PayPal button not found inside iframe.")

    finally:
        time.sleep(3)
        driver.quit()
        print("INFO: Browser closed.")

# Main runner
if __name__ == "__main__":
    test_shipping_and_paypal_button()
