from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

# Open Google Maps
driver.get('https://www.google.com/maps')
driver.maximize_window()
driver.refresh()

# Perform search
search_box = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, "q"))
)
search_box.send_keys("Laptop Shop Near Mirpur")
search_box.send_keys(Keys.RETURN)

# Wait for results to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc"))
)

# Click on "Results" header to enable keyboard scrolling
results_header = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "fontTitleLarge"))
)
results_header.click()
time.sleep(2)

# Scroll and load more shops using keyboard keys
for _ in range(80):  # Adjust the range for more scrolling
    ActionChains(driver).send_keys(Keys.DOWN).perform()
    time.sleep(0.2)

# Collect shop links (Limit to 30 shops)
shop_links = [shop.get_attribute('href') for shop in driver.find_elements(
    By.CLASS_NAME, 'hfpxzc')][:30]

# Dictionary to store results
shops_data = []

# Visit each shop page to extract details
for link in shop_links:
    driver.get(link)

    # Wait for shop details to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'Io6YTe.fontBodyMedium.kR99db.fdkmkc'))
    )

    # Extract shop name
    try:
        shop_name = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "DUwDvf.lfPIob"))
        ).text
    except:
        shop_name = "N/A"

    # Extract location
    try:
        location = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "Io6YTe.fontBodyMedium.kR99db.fdkmkc"))
        ).text
    except:
        location = "N/A"

    # Extract phone number
    try:
        phone_number = "N/A"
        main_class = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'AeaXub'))
        )
        text = " ".join([j.text for j in main_class])
        phone_matches = re.findall(r'\d{5}-\d{6}', text)
        phone_number = phone_matches[0] if phone_matches else "N/A"
    except:
        phone_number = "N/A"

    # Extract website URL
    try:
        website_url = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[6]/a')
            )
        ).get_attribute('href')
    except:
        website_url = "N/A"

    # Store extracted data
    shops_data.append({
        "name": shop_name,
        "location": location,
        "phone": phone_number,
        "website": website_url
    })

    print(f"""Collected: {
          shop_name} - {location} - {phone_number} - {website_url}""")

    # Return to the search results
    # time.sleep(200)
    driver.back()
    time.sleep(2)

# Print final collected data
for idx, shop in enumerate(shops_data, 1):
    print(f"Shop {idx}:")
    print(f"Name: {shop['name']}")
    print(f"Location: {shop['location']}")
    print(f"Phone: {shop['phone']}")
    print(f"Website: {shop['website']}")
    print("-" * 40)

# Close browser
driver.quit()
