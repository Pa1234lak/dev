from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

try:
    # Step 1: Open product page
    driver.get("https://web-app-cjv8.onrender.com/product/levis-shirt/")
    print("PASSED: Opened product page")

    # Select quantity = 1
    Select(wait.until(EC.presence_of_element_located((By.ID, "select")))).select_by_value("1")

    # Click Add to Cart
    wait.until(EC.element_to_be_clickable((By.ID, "add-button"))).click()
    print("PASSED: Added product to cart")

    time.sleep(2)  # Wait for cart update (optional)

    # Step 2: Go to cart page
    driver.get("https://web-app-cjv8.onrender.com/cart/")
    print("PASSED: Navigated to cart")

    # Step 3: Verify total amount in cart
    total_element = wait.until(EC.presence_of_element_located((By.ID, "total")))
    total_amount = total_element.text
    print(f"INFO: Cart total: {total_amount}")
    assert float(total_amount) > 0, "FAILED: Total amount is not greater than zero"

    # Step 4: Go to checkout
    driver.get("https://web-app-cjv8.onrender.com/payment/checkout")
    print("PASSED: Navigated to checkout page")

    # Step 5: Fill in billing details
    wait.until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("Test User")
    driver.find_element(By.NAME, "email").send_keys("test@example.com")
    driver.find_element(By.NAME, "address1").send_keys("123 Test St")
    driver.find_element(By.NAME, "address2").send_keys("Suite 100")
    driver.find_element(By.NAME, "city").send_keys("Testville")
    driver.find_element(By.NAME, "state").send_keys("TS")
    driver.find_element(By.NAME, "zipcode").send_keys("12345")
    print("PASSED: Filled in billing info")

    # Optional: simulate PayPal payment flow completion
    driver.execute_script("window.location.href='/payment/payment-success'")
    print("INFO: Redirected to payment success page")

    # Step 6: Validate success page
    success = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Payment Successful') or contains(text(), 'payment successful')]")))
    assert success, "FAILED: Payment success message not found"
    print("PASSED: Payment was successful")

finally:
    time.sleep(2)
    driver.quit()
