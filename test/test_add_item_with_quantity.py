from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Step 1: Setup Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

try:
    # Step 2: Open product page
    driver.get("https://web-app-cjv8.onrender.com/product/levis-shirt/")
    print("PASSED: Opened product page")

    # Step 3: Select quantity = 2
    quantity_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='select']")))
    Select(quantity_dropdown).select_by_value("2")
    print("PASSED: Selected quantity 2")

    # Step 4: Click "Add to Cart" button
    add_button = wait.until(EC.element_to_be_clickable((By.ID, "add-button")))
    add_button.click()
    print("PASSED: Clicked Add to Cart")

    # Step 5: Wait for cart to update
    cart_qty = wait.until(EC.presence_of_element_located((By.ID, "cart-qty")))
    time.sleep(2)  # allow time for AJAX cart update
    cart_count = int(cart_qty.text)
    print(f"INFO: Cart quantity shown: {cart_count}")

    # Step 6: Assert quantity is correct
    assert cart_count == 2, f"FAILED: Expected cart quantity 2 but got {cart_count}"
    print("PASSED: Cart quantity is correct.")

finally:
    driver.quit()
