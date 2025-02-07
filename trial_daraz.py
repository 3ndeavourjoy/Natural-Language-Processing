from selenium import webdriver
import time
import re
import math
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Edge()

save_dict = {}

driver.get("https://www.daraz.com.bd/routers/?page=1")
driver.maximize_window()

# Get total number of products and calculate pages
wait = WebDriverWait(driver, 15)
total_number_text = wait.until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'div.Ck3Nt > div > div > span:nth-child(1)')
)).text

# Extract total number of products
total_products = int(re.findall(r'\d+', total_number_text)[0])
total_pages = math.ceil(total_products / 40)
print(f"Total Products: {total_products}, Total Pages: {total_pages}")

# Loop through each page
for page_no in range(1, total_pages + 1):
    driver.get(f"https://www.daraz.com.bd/routers/?page={page_no}")
    time.sleep(5)  # Small delay for page load

    # Get all product elements dynamically
    product_elements = driver.find_elements(By.CSS_SELECTOR, "div._17mcb > div")
    print(f"Page {page_no} - Found {len(product_elements)} products")

    product_links = []
    
    # Loop through available products only
    for prod_index, product in enumerate(product_elements, start=1):
        try:
            link_element = product.find_element(By.CSS_SELECTOR, "div.ICdUp > div > a")
            link = link_element.get_attribute("href")
            product_links.append(link)
        except Exception as e:
            print(f"Skipping product {prod_index} on page {page_no} due to error: {e}")

    # Store results in dictionary
    save_dict[f"page_{page_no}"] = product_links

# Print extracted product links
for page, links in save_dict.items():
    print(f"{page}: {', '.join(links)}")

# Print total scraped product count
total_links = sum(len(links) for links in save_dict.values())
print(f"Total products scraped: {total_links}")

time.sleep(5)
driver.quit()
