from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.114 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)


driver.get('https://www.daraz.com.bd/products/4g-wifi-i468701703-s2256167219.html')
driver.maximize_window()
time.sleep(20)


height = driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
    time.sleep(0.2)

    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height==height:
        break
    height=new_height



product_info = {}

product_name = driver.find_element(By.XPATH, '//*[@id="module_product_title_1"]/div/div/h1').text
product_info['product_name'] = product_name



price = driver.find_element(By.XPATH, '//*[@id="module_product_price_1"]/div/div/span').text
product_info['price'] = price


product_details = driver.find_element(By.XPATH, '//*[@id="module_product_detail"]/div/div/div[1]/div[1]/ul/li').text
product_info['product_details'] = product_details


image = driver.find_element(By.XPATH, '//*[@id="module_item_gallery_1"]/div/div[1]/div/img').get_attribute('src')
product_info['image'] = image

print(product_info)

driver.quit()