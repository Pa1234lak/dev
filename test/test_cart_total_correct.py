from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

# Step 1: Setup Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

try:
    # Step 2: Open product page
    driver.get("https://web-app-cjv8.onrender.com/product/levis-shirt/")
    print("✅ Opened product page")

    # Step 3: Select quantity = 2
    quantity_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='select']")))
    Select(quantity_dropdown).select_by_value("2")
    print("✅ Selected quantity 2")

    # Step 4: Click "Add to Cart" button
    add_button = wait.until(EC.element_to_be_clickable((By.ID, "add-button")))
    add_button.click()
    print("✅ Clicked Add to Cart")

    # Step 5: Wait for cart to update
    cart_qty = wait.until(EC.presence_of_element_located((By.ID, "cart-qty")))
    time.sleep(2)  # allow time for AJAX cart update
    print(f"🛒 Cart quantity shown: {cart_qty.text}")

    # Step 6: Go to cart page
    driver.get("https://web-app-cjv8.onrender.com/cart/")
    print("✅ Navigated to cart page")

    # Step 7: Wait and get the total amount with ₹ symbol
    total_elem = wait.until(EC.presence_of_element_located((By.ID, "total")))
    total_text = total_elem.text
    print(f"💰 Total text found: {total_text}")

    # Step 8: Extract numeric value and validate
    match = re.search(r'₹\s*([\d\.]+)', total_text)
    assert match, "❌ ₹ symbol or total not found!"
    total = float(match.group(1))
    assert total > 0, f"❌ Expected total > 0 but got {total}"
    print(f"✅ Cart total is ₹{total} — test passed.")

finally:
    driver.quit()
