from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Setup
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    # 1. Open the product page
    driver.get("https://web-app-cjv8.onrender.com/product/levis-shirt/")

    # 2. Wait for and set the quantity input
    quantity_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='number']"))
    )
    quantity_input.clear()
    quantity_input.send_keys("2")
    print("SUCCESS: Quantity set to 2.")

    # 3. Click on "Add to Cart" button
    add_to_cart_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add to Cart')]"))
    )
    add_to_cart_btn.click()
    print("SUCCESS: Clicked 'Add to Cart'.")

    # 4. Go to the cart page
    time.sleep(1)  # slight delay in case redirect is slow
    driver.get("https://web-app-cjv8.onrender.com/cart/")

    # 5. Verify Levi's Shirt with quantity 2 is in the cart
    product_name = wait.until(
        EC.presence_of_element_located((By.XPATH, "//td[contains(text(), \"Levi's Shirt\")]"))
    )
    quantity_cell = product_name.find_element(By.XPATH, "../td[2]")  # Assuming quantity is in next column

    if quantity_cell.text.strip() == "2":
        print("SUCCESS: Correct quantity (2) for Levi's Shirt found in cart.")
    else:
        print(f"FAILED: Quantity mismatch. Found: {quantity_cell.text.strip()}")

except TimeoutException as e:
    print(f"FAILED: Timeout waiting for element - {str(e)}")

finally:
    time.sleep(3)
    driver.quit()
