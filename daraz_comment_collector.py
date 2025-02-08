from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)


# Daraz product review page URL
# Has 168 reviews
# url = "https://www.daraz.com.bd/products/mercusys-mw306r-300mbps-multi-mode-wireless-n-router-i261635130.html"
# Has 20 reviews
url = "https://www.daraz.com.bd/products/lte-wifi-150-mbps-usb-i331927284.html"
# this url has no reviews, for testing this could be use
# url = "https://www.daraz.com.bd/products/ac1200-wifi-mu-mimo-i458384103-s2197820609.html"
driver.get(url)
driver.maximize_window()

# Refresh to ensure full data load
driver.refresh()

#  Check if the product has ratings
try:
    rating_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".pdp-review-summary__link"))
    )
    rating_text = rating_element.text.strip()

    if "No Ratings" in rating_text:
        print("No ratings available for this product. Skipping scraping.")
        driver.quit()
        exit()
    else:
        print(f"Product has {rating_text}. Proceeding with scraping.")

        # Scroll down 1200px to load reviews
        driver.execute_script("window.scrollBy(0, 1200);")
        time.sleep(2)

except Exception as e:
    print("Error checking product ratings:", e)
    driver.quit()
    exit()


# Function to scrape reviews from the current page
def scrape_reviews():
    reviews = []
    # Full star image URL
    full_star_url = "//img.lazcdn.com/g/tps/tfs/TB19ZvEgfDH8KJjy1XcXXcpdXXa-64-64.png"

    # Locate all review elements
    review_elements = driver.find_elements(By.CSS_SELECTOR, ".item")

    for review in review_elements:
        try:
            # Extract username
            username = review.find_element(
                By.CSS_SELECTOR, ".middle span").text

            # Extract stars
            stars = 0
            star_elements = review.find_elements(
                By.CSS_SELECTOR, ".container-star .star")
            for star in star_elements:
                star_url = star.get_attribute("src")
                if full_star_url in star_url:
                    stars += 1  # Count only full stars

            # Extract date
            date = review.find_element(By.CSS_SELECTOR, ".top .title").text

            # Extract review text
            review_text = review.find_element(By.CSS_SELECTOR, ".content").text

            reviews.append({
                "username": username,
                "rating": stars,
                "date": date,
                "review_text": review_text
            })
        except Exception as e:
            print("Error extracting review:", e)

    return reviews


# Main loop to scrape all pages
all_reviews = []

while True:
    all_reviews.extend(scrape_reviews())

    try:
        # Wait for the "Next" button
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '//*[@id ="module_product_review"]/div/div/div[3]/div[2]/div/button[2]')
            )
        )

        # Check if the button is disabled (last page)
        if "disabled" in next_button.get_attribute("class"):
            print("No more pages to load.")
            break

        # Click the "Next" button
        next_button.click()
        time.sleep(3)  # Allow time for new reviews to load

    except Exception:
        print("Pagination finished or button not found.")
        break

# Close browser
driver.quit()

# Print collected reviews
for review in all_reviews:
    print(review)
    print("-" * 40)

print("Total reviews:", len(all_reviews))
