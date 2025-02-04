from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--incognito")

# Initialized the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Maximized the browser window
driver.maximize_window()

try:
    url = "https://www.daraz.com.bd/products/tp-link-tl-wr820n-v2-300-mbps-multi-mode-wi-fi-router-i133488288-s1055188633.html"
    driver.get(url)

    # Wait for 1 seconds
    time.sleep(1)

    # Reload the page
    driver.refresh()

    # Wait for 1 seconds
    time.sleep(1)

    # Collect product data
    wait = WebDriverWait(driver, 10)

    # Product Name
    product_name = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="module_product_title_1"]/div/div/h1'))).text

    # Price
    price = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="module_product_price_1"]/div/div/span'))).text

    # Image URL
    image_url = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="module_item_gallery_1"]/div/div[1]/div/img'))).get_attribute('src')

    # Ratings (optional)
    try:
        ratings = driver.find_element(
            By.XPATH, '//*[@id="module_product_review_star_1"]/div/a[1]').text
    except:
        ratings = None

    # Questions Answered (optional)
    try:
        questions_answered = driver.find_element(
            By.XPATH, '//*[@id="module_product_review_star_1"]/div/a[2]').text
    except:
        questions_answered = None

    # Get the current scroll height
    scroll_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down 300px
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(1)  # Wait for content to load if necessary

    # Product Details
    details_section = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="module_product_detail"]/div/div/div[1]/div[1]')))
    details = [li.text for li in details_section.find_elements(
        By.TAG_NAME, 'li')]

    # Output the collected data
    product_data = {
        'Product Name': product_name,
        'Price': price,
        'Image URL': image_url,
        'Ratings': ratings,
        'Questions Answered': questions_answered,
        'Product Details': details
    }

    for key, value in product_data.items():
        print(f"{key}: {value}")

finally:
    driver.quit()
