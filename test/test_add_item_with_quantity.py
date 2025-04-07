from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

try:
    # Step 1: Open product page
    driver.get("https://web-app-cjv8.onrender.com/product/levis-shirt/")
    print("✅ Opened product page.")

    # Step 2: Select quantity = 2
    quantity_dropdown = wait.until(
        EC.presence_of_element_located((By.ID, "select"))
    )
    Select(quantity_dropdown).select_by_value("2")
    print("✅ Selected quantity 2.")

    # Step 3: Click Add to Cart
    add_button = wait.until(EC.element_to_be_clickable((By.ID, "add-button")))
    add_button.click()
    print("✅ Clicked Add to Cart.")

    # Step 4: Wait for AJAX/cart update
    time.sleep(2)

    # Step 5: Visit the cart page
    driver.get("https://web-app-cjv8.onrender.com/cart/")
    print("✅ Navigated to cart page.")

    # Step 6: Validate cart quantity
    try:
        cart_qty_elem = wait.until(EC.presence_of_element_located((By.ID, "cart-qty")))
        cart_qty = cart_qty_elem.text.strip()
        if cart_qty == "2":
            print("✅ Cart quantity is correct (2).")
        else:
            print(f"❌ Cart quantity mismatch: Found {cart_qty}, expected 2.")
    except TimeoutException:
        print("❌ Could not find 'cart-qty' element.")

    # Step 7: Validate total price is visible and greater than zero
    try:
        total_elem = wait.until(EC.presence_of_element_located((By.ID, "total")))
        total = total_elem.text.strip()
        if total and float(total.replace("$", "").replace("₹", "")) > 0:
            print(f"🎉 SUCCESS: Total is visible and valid — {total}")
        else:
            print(f"❌ Total value invalid or zero — found: {total}")
    except TimeoutException:
        print("❌ Could not find 'total' element.")

except TimeoutException as e:
    print(f"❌ TimeoutException: {e}")

finally:
    time.sleep(2)
    driver.quit()
