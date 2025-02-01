from selenium import webdriver
from selenium.webdriver.common.by import By

import re
import time


def get_total_pages(driver, url):
    driver.get(url)
    time.sleep(3)

    total_items_text = driver.find_element(
        By.CSS_SELECTOR, "#root > div > div.ant-row.FrEdP.css-1bkhbmc.app > div:nth-child(1) > div > div.ant-col.ant-col-20.ant-col-push-4.Jv5R8.css-1bkhbmc.app > div.xYcXp > div > div.Ck3Nt > div > div > span:nth-child(1)").text
    # Extract the number using regex
    total_items = int(re.search(r'\d+', total_items_text).group())
    total_pages = round(total_items / 40)
    print(f"Total items found: {total_items}")
    print(f"Total pages calculated: {total_pages}")
    return total_pages


def get_product_links(driver, url, total_pages):
    result = {}
    for page in range(1, total_pages + 1):
        page_url = f"{url}?page={page}"
        driver.get(page_url)
        time.sleep(3)

        product_links = []
        for i in range(1, 41):  # Iterate from 1 to 40
            try:
                selector = f"""#root > div > div.ant-row.FrEdP.css-1bkhbmc.app > div:nth-child(1) > div > div.ant-col.ant-col-20.ant-col-push-4.Jv5R8.css-1bkhbmc.app > div._17mcb > div:nth-child({
                    i}) > div > div > div.ICdUp > div > a"""
                product_element = driver.find_element(
                    By.CSS_SELECTOR, selector)
                link = product_element.get_attribute("href")
                product_links.append(link)
            except Exception as e:
                print(f"Element {i} not found on page {page}: {e}")
                continue

        result[f"page_{page}"] = product_links
        print(f"Scraped {len(product_links)} links from page {page}")
    return result


def main():
    url = "https://www.daraz.com.bd/routers/"
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        total_pages = get_total_pages(driver, url)
        product_data = get_product_links(driver, url, total_pages)
        print("Final scraped data:", product_data)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
