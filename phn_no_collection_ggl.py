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
for _ in range(200):  # Adjust the range for more scrolling
    ActionChains(driver).send_keys(Keys.DOWN).perform()
    time.sleep(0.4)

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

print(shop_links, len(shop_links))
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


# example output
"""
['https://www.google.com/maps/place/%E0%A6%B2%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%AA%E0%A6%9F%E0%A6%AA+%E0%A6%93%E0%A6%AF%E0%A6%BC%E0%A6%BE%E0%A6%B0%E0%A7%8D%E0%A6%B2%E0%A7%8D%E0%A6%A1+%E0%A6%AC%E0%A6%BF%E0%A6%A1%E0%A6%BF/data=!4m7!3m6!1s0x3755c0d692c00001:0x8c8cbee90af0151c!8m2!3d23.8064168!4d90.3695264!16s%2Fg%2F11h_vvkhdk!19sChIJAQDAktbAVTcRHBXwCum-jIw?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%8F%E0%A6%B8%E0%A6%8F%E0%A6%B8+%E0%A6%95%E0%A6%AE%E0%A7%8D%E0%A6%AA%E0%A6%BF%E0%A6%89%E0%A6%9F%E0%A6%BE%E0%A6%B0+%7C+%E0%A6%AE%E0%A6%BF%E0%A6%B0%E0%A6%AA%E0%A7%81%E0%A6%B0-10/data=!4m7!3m6!1s0x3755c1fdeb5c3bbf:0x23a36af34a532d0!8m2!3d23.8065524!4d90.36971!16s%2Fg%2F11lbxwsbr2!19sChIJvztc6_3BVTcR0DKlNK82OgI?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%95%E0%A6%BE%E0%A6%9C%E0%A7%80+%E0%A6%9F%E0%A7%87%E0%A6%95%E0%A6%A8%E0%A7%8B%E0%A6%B2%E0%A6%9C%E0%A6%BF/data=!4m7!3m6!1s0x3755c0d692206ed5:0xf53955f178dc46ef!8m2!3d23.8066302!4d90.3690243!16s%2Fg%2F11gbzcmw5t!19sChIJ1W4gktbAVTcR70bcePFVOfU?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%93%E0%A6%AF%E0%A6%BC%E0%A6%BE%E0%A6%B0%E0%A7%8D%E0%A6%B2%E0%A7%8D%E0%A6%A1+%E0%A6%95%E0%A6%AE%E0%A7%8D%E0%A6%AA%E0%A6%BF%E0%A6%89%E0%A6%9F%E0%A6%BE%E0%A6%B0+%E0%A6%B8%E0%A6%BF%E0%A6%B8%E0%A7%8D%E0%A6%9F%E0%A7%87%E0%A6%AE/data=!4m7!3m6!1s0x3755c0d986915a5b:0x68c09c2ac0572f78!8m2!3d23.8066302!4d90.3690243!16s%2Fg%2F11c2lgpm14!19sChIJW1qRhtnAVTcReC9XwCqcwGg?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%B2%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%AA%E0%A6%9F%E0%A6%AA.%E0%A6%B8%E0%A7%8B%E0%A6%B0%E0%A7%8D%E0%A6%B8/data=!4m7!3m6!1s0x3755c17507408cb1:0x7a2c2e1cef798adc!8m2!3d23.8048078!4d90.3693214!16s%2Fg%2F11sh00sz89!19sChIJsYxAB3XBVTcR3Ip57xwuLHo?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%87%E0%A6%89+%E0%A6%9F%E0%A7%87%E0%A6%95+%E0%A6%AC%E0%A6%BF%E0%A6%A1%E0%A7%80/data=!4m7!3m6!1s0x3755c0b7c93ec59b:0x1f9ebda108706a47!8m2!3d23.8057465!4d90.3685768!16s%2Fg%2F12lr_8z4f!19sChIJm8U-ybfAVTcRR2pwCKG9nh8?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%87%E0%A6%9F+%E0%A6%AC%E0%A6%BF%E0%A6%A1%E0%A6%BF+%E0%A6%B6%E0%A6%AA/data=!4m7!3m6!1s0x3755c1d4eefc6ac1:0x8bbea2b6bd8edee1!8m2!3d23.8061817!4d90.3681095!16s%2Fg%2F11qrt7877p!19sChIJwWr87tTBVTcR4d6Ovbaivos?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%97%E0%A7%8D%E0%A6%B0%E0%A6%BF%E0%A6%A8+%E0%A6%9F%E0%A7%87%E0%A6%95%E0%A6%A8%E0%A7%8B%E0%A6%B2%E0%A6%9C%E0%A6%BF/data=!4m7!3m6!1s0x3755c19d7d8acd05:0x2dc0062b6175cefe!8m2!3d23.7991441!4d90.3528902!16s%2Fg%2F11gjx12f8n!19sChIJBc2KfZ3BVTcR_s51YSsGwC0?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%97%E0%A6%AE+%E0%A6%9F%E0%A7%87%E0%A6%95/data=!4m7!3m6!1s0x3755c77952904999:0x6aa525ae586dcb87!8m2!3d23.8380143!4d90.3755704!16s%2Fg%2F11n6wtp562!19sChIJmUmQUnnHVTcRh8ttWK4lpWo?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%B2%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%AA%E0%A6%9F%E0%A6%AA+%E0%A6%9F%E0%A7%87%E0%A6%B0%E0%A6%BF%E0%A6%9F%E0%A7%8B%E0%A6%B0%E0%A6%BF/data=!4m7!3m6!1s0x3755c1a619ea7619:0x2c1024a455ea0cc3!8m2!3d23.8064171!4d90.3695265!16s%2Fg%2F11t40hg8pz!19sChIJGXbqGabBVTcRwwzqVaQkECw?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/Maraya+Global+%28Mirpur+Branch%29/data=!4m7!3m6!1s0x3755c1005f76a8a5:0x464d32e20e49166e!8m2!3d23.8061328!4d90.3698309!16s%2Fg%2F11wj6xgh_x!19sChIJpah2XwDBVTcRbhZJDuIyTUY?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%B2%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%AA%E0%A6%9F%E0%A6%AA+%E0%A6%B2%E0%A6%BE%E0%A6%89%E0%A6%9E%E0%A7%8D%E0%A6%9C/data=!4m7!3m6!1s0x3755c127c805023d:0xa81697ca2189d53f!8m2!3d23.8064347!4d90.3701497!16s%2Fg%2F11vyytrzh_!19sChIJPQIFyCfBVTcRP9WJIcqXFqg?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%A8%E0%A7%87%E0%A6%95%E0%A7%8D%E0%A6%B8%E0%A6%BE%E0%A6%B8+%E0%A6%95%E0%A6%AE%E0%A7%8D%E0%A6%AA%E0%A6%BF%E0%A6%89%E0%A6%9F%E0%A6%BE%E0%A6%B0+~+%E0%A6%86%E0%A6%87%E0%A6%A1%E0%A6%BF%E0%A6%AC%E0%A6%BF/data=!4m7!3m6!1s0x3755c74c27bb8ff7:0xa03907452af45284!8m2!3d23.7783624!4d90.3795762!16s%2Fg%2F11f3zt6w9b!19sChIJ94-7J0zHVTcRhFL0KkUHOaA?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%85%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%AA%E0%A7%8B%E0%A6%B2%E0%A7%8B+%E0%A6%97%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%9C%E0%A7%87%E0%A6%9F/data=!4m7!3m6!1s0x3755c164bcbb6569:0x102eecd8ec7ec22a!8m2!3d23.8057261!4d90.3677736!16s%2Fg%2F11rtvmnqrv!19sChIJaWW7vGTBVTcRKsJ-7NjsLhA?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/Laptop+House+BD/data=!4m7!3m6!1s0x3755c1714b31d757:0xedf34c994414d5b5!8m2!3d23.8062999!4d90.3678818!16s%2Fg%2F11j305bn8z!19sChIJV9cxS3HBVTcRtdUURJlM8-0?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%86%E0%A6%B0+%E0%A6%95%E0%A6%AE%E0%A7%8D%E0%A6%AA%E0%A6%BF%E0%A6%89%E0%A6%9F%E0%A6%BE%E0%A6%B0%E0%A7%8D%E0%A6%B8/data=!4m7!3m6!1s0x3755c0d692b2204f:0xb1dd0520e761f525!8m2!3d23.8066118!4d90.369202!16s%2Fg%2F11cjj55mwz!19sChIJTyCyktbAVTcRJfVh5yAF3bE?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%8F%E0%A6%AE%E0%A6%B8%E0%A6%BF+%E0%A6%B8%E0%A6%B2%E0%A6%BF%E0%A6%89%E0%A6%B6%E0%A6%A8+%E0%A6%AC%E0%A6%BF%E0%A6%A1%E0%A6%BF+%28+%E0%A6%AE%E0%A6%BF%E0%A6%B0%E0%A6%AA%E0%A7%81%E0%A6%B0+%E0%A6%AC%E0%A7%8D%E0%A6%B0%E0%A6%BE%E0%A6%9E%E0%A7%8D%E0%A6%9A+%29/data=!4m7!3m6!1s0x3755c152865b0fa1:0xeb912ddf4abb146e!8m2!3d23.8062922!4d90.3692771!16s%2Fg%2F11pcw_lm96!19sChIJoQ9bhlLBVTcRbhS7St8tkes?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%A4%E0%A6%BE%E0%A6%95%E0%A6%93%E0%A6%AF%E0%A6%BC%E0%A6%BE+%E0%A6%B2%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%AA%E0%A6%9F%E0%A6%AA+%E0%A6%9C%E0%A6%A8%E0%A7%87/data=!4m7!3m6!1s0x3755c12f2a3b5a79:0x305e46a50a2a672d!8m2!3d23.8216322!4d90.378171!16s%2Fg%2F11t859gd2l!19sChIJeVo7Ki_BVTcRLWcqCqVGXjA?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%AA%E0%A7%8D%E0%A6%B2%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%A8%E0%A7%87%E0%A6%9F+%E0%A6%87%E0%A6%9F+%E0%A6%AC%E0%A6%BF%E0%A6%A1%E0%A6%BF/data=!4m7!3m6!1s0x3755c133bae75af9:0x983c52a985ee35f0!8m2!3d23.8058214!4d90.3681436!16s%2Fg%2F11j4wjlcvt!19sChIJ-VrnujPBVTcR8DXuhalSPJg?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%B2%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%AA%E0%A6%9F%E0%A6%AA+%E0%A6%B8%E0%A7%8D%E0%A6%9F%E0%A7%87%E0%A6%B6%E0%A6%A8/data=!4m7!3m6!1s0x3755c121814befad:0x5cd59c0601c8acdb!8m2!3d23.806049!4d90.3681469!16s%2Fg%2F11v05cl6ld!19sChIJre9LgSHBVTcR26zIAQac1Vw?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%95%E0%A6%AE%E0%A7%8D%E0%A6%AA%E0%A6%BF%E0%A6%89%E0%A6%9F%E0%A6%BE%E0%A6%B0+%E0%A6%95%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%B8%E0%A6%B2/data=!4m7!3m6!1s0x3755c0d692c8058d:0xc6efcda65084cab8!8m2!3d23.8068552!4d90.3690349!16s%2Fg%2F11b7q2pm2s!19sChIJjQXIktbAVTcRuMqEUKbN78Y?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%86%E0%A6%AC%E0%A7%8D%E0%A6%A6%E0%A7%81%E0%A6%B2%E0%A7%8D%E0%A6%B2%E0%A6%BE%E0%A6%B9+%E0%A6%95%E0%A6%AE%E0%A7%8D%E0%A6%AA%E0%A6%BF%E0%A6%89%E0%A6%9F%E0%A6%BE%E0%A6%B0+%E0%A6%B8%E0%A6%BE%E0%A7%9F%E0%A7%87%E0%A6%A8%E0%A7%8D%E0%A6%B8/data=!4m7!3m6!1s0x3755c0d6ecd5451b:0xb3b7d2d055e4f367!8m2!3d23.8066302!4d90.3690243!16s%2Fg%2F1jkwd1fdv!19sChIJG0XV7NbAVTcRZ_PkVdDSt7M?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/21+%E0%A6%9F%E0%A7%87%E0%A6%95%E0%A6%A8%E0%A7%8B%E0%A6%B2%E0%A6%9C%E0%A6%BF/data=!4m7!3m6!1s0x3755c7bc6bb0c7f5:0x818a61a6f3cf1ddd!8m2!3d23.8062797!4d90.3690347!16s%2Fg%2F11h39ymk0b!19sChIJ9cewa7zHVTcR3R3P86ZhioE?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%87%E0%A6%89%E0%A6%A8%E0%A6%BF%E0%A6%AD%E0%A6%BE%E0%A6%B0%E0%A7%8D%E0%A6%B8+%E0%A6%95%E0%A6%AE%E0%A7%8D%E0%A6%AA%E0%A6%BF%E0%A6%89%E0%A6%9F%E0%A6%BE%E0%A6%B0+%E0%A6%95%E0%A7%87%E0%A7%9F%E0%A6%BE%E0%A6%B0/data=!4m7!3m6!1s0x3755c0d69219d2d9:0x89b217abbe577ee4!8m2!3d23.8066416!4d90.36921!16s%2Fg%2F11f_zm09lc!19sChIJ2dIZktbAVTcR5H5XvqsXsok?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%87%E0%A6%89%E0%A6%A8%E0%A6%BF%E0%A6%AD%E0%A6%BE%E0%A6%B0%E0%A7%8D%E0%A6%B8+%E0%A6%87%E0%A6%9F/data=!4m7!3m6!1s0x3755c7b16bc7bca9:0xfa9bcc1d3c11dd95!8m2!3d23.8197687!4d90.3778961!16s%2Fg%2F11pvwzn9fl!19sChIJqbzHa7HHVTcRld0RPB3Mm_o?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%95%E0%A6%AE%E0%A7%8D%E0%A6%AA%E0%A6%BF%E0%A6%89%E0%A6%9F%E0%A6%BE%E0%A6%B0+%E0%A6%AA%E0%A6%AF%E0%A6%BC%E0%A7%87%E0%A6%A8%E0%A7%8D%E0%A6%9F/data=!4m7!3m6!1s0x3755c0e880f03f13:0x3e7a85782d8be049!8m2!3d23.7981785!4d90.3536896!16s%2Fg%2F11fzb07hbz!19sChIJEz_wgOjAVTcRSeCLLXiFej4?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/Treematrik/data=!4m7!3m6!1s0x3755c13af199c295:0xcbffaf51c4411c44!8m2!3d23.8247259!4d90.3638895!16s%2Fg%2F11fz9z6hqv!19sChIJlcKZ8TrBVTcRRBxBxFGv_8s?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%932+%E0%A6%9F%E0%A7%8D%E0%A6%B0%E0%A7%87%E0%A6%A1+%E0%A6%87%E0%A6%A8%E0%A7%8D%E0%A6%9F%E0%A6%BE%E0%A6%B0%E0%A6%A8%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%B6%E0%A6%A8%E0%A6%BE%E0%A6%B2/data=!4m7!3m6!1s0x3755c0d6f3cc1b05:0x9b22bf70261e9cbc!8m2!3d23.806931!4d90.368709!16s%2Fg%2F11gfh_bzpr!19sChIJBRvM89bAVTcRvJweJnC_Ips?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%86%E0%A6%B0+%E0%A6%95%E0%A6%AE%E0%A7%8D%E0%A6%AA%E0%A6%BF%E0%A6%89%E0%A6%9F%E0%A6%BE%E0%A6%B0+%E0%A6%AA%E0%A7%8D%E0%A6%B2%E0%A6%BE%E0%A6%B8/data=!4m7!3m6!1s0x3755c1c4f8ade5ab:0x123aa50fc8147282!8m2!3d23.8159634!4d90.3668719!16s%2Fg%2F11h0qz6ll_!19sChIJq-Wt-MTBVTcRgnIUyA-lOhI?authuser=0&hl=bn&rclk=1', 'https://www.google.com/maps/place/%E0%A6%AB%E0%A6%BE%E0%A6%B0%E0%A7%81%E0%A6%95+%E0%A6%87%E0%A6%9F+%E0%A6%B8%E0%A6%B2%E0%A6%BF%E0%A6%89%E0%A6%B6%E0%A6%A8/data=!4m7!3m6!1s0x3755c186c51560b3:0x29e5aa26370f32de!8m2!3d23.8055631!4d90.3689697!16s%2Fg%2F11fjmg2586!19sChIJs2AVxYbBVTcR3jIPNyaq5Sk?authuser=0&hl=bn&rclk=1'] 30
Shop 1:
Name: ল্যাপটপ ওয়ার্ল্ড বিডি
Location: Shop -08, Level- 02, Dewan Market, মিরপুর ১০ নং গোলচত্বর, ঢাকা 1216
Phone: 01861-999948
Website: http://laptopworldbd.com/
----------------------------------------
Shop 2:
Name: এসএস কম্পিউটার | মিরপুর-10
Location: House 07, Road 03,Harun super market (2nd floor, মিরপুর ১০ নং গোলচত্বর, ঢাকা 1216
Phone: 01643-946107
Website: N/A
----------------------------------------
Shop 3:
Name: কাজী টেকনোলজি
Location: 5th Floor, Shop No: 49 80/A, শাহ্‌ আলি প্লাজা, মিরপুর ১০ নং গোলচত্বর, ঢাকা 1216
Phone: N/A
Website: N/A
----------------------------------------
Shop 4:
Name: ওয়ার্ল্ড কম্পিউটার সিস্টেম
Location: Shop no 702, 6th Floor, শাহ্‌ আলি প্লাজা, ঢাকা 1216
Phone: 01618-927565
Website: http://www.wcs.com.bd/
----------------------------------------
Shop 5:
Name: ল্যাপটপ.সোর্স
Location: No 255 ,107 4th Floor, Sony Bhaban, Shenpara Parbata ,Metro Piller, ঢাকা 1216
Phone: 01724-406156
Website: N/A
----------------------------------------
Shop 6:
Name: ইউ টেক বিডী
Location: Section-06, House-93,Level-3.Road-2, 10 Boundary Rd, ঢাকা 1216
Phone: 01711-385849
Website: N/A
----------------------------------------
Shop 7:
Name: ইট বিডি শপ
Location: R949+F6, ঢাকা 1216
Phone: 01710-913417
Website: N/A
----------------------------------------
Shop 8:
Name: গ্রিন টেকনোলজি
Location: 3rd floor , shop 406, Mukto Bangla Shopping Complex, number bus stand, ঢাকা 1216
Phone: 01315-090371
Website: N/A
----------------------------------------
Shop 9:
Name: গম টেক
Location: Mirpur DOHS Shopping complex,Shop-20,Level-5, Road 9 Sagufta, ঢাকা 1216
Phone: 01618-216141
Website: https://www.gamotech.com.bd/
----------------------------------------
Shop 10:
Name: ল্যাপটপ টেরিটোরি
Location: Level- 2, Shop No. 08, Dewan Market, মিরপুর ১০ নং গোলচত্বর, ঢাকা 1216
Phone: 01779-811661
Website: N/A
----------------------------------------
Shop 11:
Name: Maraya Global (Mirpur Branch)
Location: House No, Zahanara Villa, 07 Road No-04, ঢাকা 1216
Phone: 01606-590629
Website: N/A
----------------------------------------
Shop 12:
Name: ল্যাপটপ লাউঞ্জ
Location: Shop No: 2, Road No: 3, House:12 Chadni Plaza, ঢাকা 1216
Phone: 01631-898580
Website: N/A
----------------------------------------
Shop 13:
Name: নেক্সাস কম্পিউটার ~ আইডিবি
Location: E/8 A, আইডিবি ভবন, 2nd Floor SR: 223/13-14, Rokeya Sharani, ঢাকা 1207
Phone: 09638-017907
Website: https://www.nexus.com.bd/
----------------------------------------
Shop 14:
Name: অ্যাপোলো গ্যাজেট
Location: Block-Kha, Holding No-2/32, Boundary Road, Block-Kha, মিরপুর ১০ নং গোলচত্বর, ঢাকা 1216
Phone: 01982-628412
Website: N/A
----------------------------------------
Shop 15:
Name: Laptop House BD
Location: Plot #12, Road#01, Section #06, Block #KHA, মিরপুর ১০ নং গোলচত্বর, ঢাকা 1216
Phone: 01773-062835
Website: http://www.laptophousebd.com/
----------------------------------------
Shop 16:
Name: আর কম্পিউটার্স
Location: Shah Ali Plaza (5th floor) Shop No 54,55, 10 বেগম রোকেয়া সরণী, ঢাকা 1216
Phone: 01631-003820
Website: http://www.wcs.com.bd/
----------------------------------------
Shop 17:
Name: এমসি সলিউশন বিডি ( মিরপুর ব্রাঞ্চ )
Location: Shop No-703, 6th Floor, শাহ্‌ আলি প্লাজা, ঢাকা 1216
Phone: 01407-056597
Website: N/A
----------------------------------------
Shop 18:
Name: তাকওয়া ল্যাপটপ জনে
Location: Block C, House 17, 11 রোড নং ৬, ঢাকা
Phone: 01708-374850
Website: N/A
----------------------------------------
Shop 19:
Name: প্ল্যানেট ইট বিডি
Location: 3rd floor sundarban courier service building, মিরপুর ১০ নং গোলচত্বর, ঢাকা 1216
Phone: 01719-706250
Website: N/A
----------------------------------------
Shop 20:
Name: ল্যাপটপ স্টেশন
Location: R949+C76, মিরপুর ১০ নং গোলচত্বর, ঢাকা 1216
Phone: 01815-807070
Website: N/A
----------------------------------------
Shop 21:
Name: কম্পিউটার ক্যাসল
Location: 5th Floor, শাহ্‌ আলি প্লাজা, Shop #8,19, 10 বেগম রোকেয়া সরণী, ঢাকা 1216
Phone: 01726-300494
Website: N/A
----------------------------------------
Shop 22:
Name: আব্দুল্লাহ কম্পিউটার সায়েন্স
Location: Shop No: 48, শাহ্‌ আলি প্লাজা, মিরপুর ১০ নং গোলচত্বর, ঢাকা 1216
Phone: 01640-888882
Website: N/A
----------------------------------------
Shop 23:
Name: 21 টেকনোলজি
Location: Sajeda Mansion, 1st floor, House No: 09, Road no: 03, মিরপুর ১০ নং গোলচত্বর, ঢাকা 1216
Phone: 01304-231600
Website: N/A
----------------------------------------
Shop 24:
Name: ইউনিভার্স কম্পিউটার কেয়ার
Location: Shah Ali Plaza, Mirpur-10, ঢাকা 1216
Phone: 01934-386987
Website: N/A
----------------------------------------
Shop 25:
Name: ইউনিভার্স ইট
Location: bazar, Bauniabad Rd, ঢাকা 1216
Phone: N/A
Website: N/A
----------------------------------------
Shop 26:
Name: কম্পিউটার পয়েন্ট
Location: Shop No: 3, Level: 4, Chowdhury Mension, 1 No. Super Market, Mirpur-1 (Beside Bus Stand), Mirpur, Dhaka 1216
Phone: 01911-266791
Website: N/A
----------------------------------------
Shop 27:
Name: Treematrik
Location: Shop- 77, Pallabi Shopping Center, Pallabi Rd, ঢাকা 1216
Phone: 01817-042433
Website: http://www.facebook.com/treematrik
----------------------------------------
Shop 28:
Name: ও2 ট্রেড ইন্টারন্যাশনাল
Location: Shop#15/A, Shah Ali Plaza, Mirpur 10, Roundabout, Mirpur, Dhaka 1216 1216
Phone: 01681-939426
Website: N/A
----------------------------------------
Shop 29:
Name: আর কম্পিউটার প্লাস
Location: House - 6, Road - 3, 11 Bus Stand, ঢাকা 1216
Phone: 01799-020349
Website: N/A
----------------------------------------
Shop 30:
Name: ফারুক ইট সলিউশন
Location: 95 বেগম রোকেয়া সরণী, ঢাকা 1216
Phone: 01995-758211
Website: N/A
----------------------------------------
"""
