from selenium import webdriver
import time
import re
import math
from selenium.webdriver.common.by import By

driver = webdriver.Edge()

save_dict = {}

driver.get("https://www.daraz.com.bd/routers/?page=1")
driver.maximize_window()

# Get the total number of pages through the website sentence
total_number_page = driver.find_element(
    By.CSS_SELECTOR,'#root > div > div.ant-row.FrEdP.css-1bkhbmc.app > div:nth-child(1) > div > div.ant-col.ant-col-20.ant-col-push-4.Jv5R8.css-1bkhbmc.app > div.xYcXp > div > div.Ck3Nt > div > div > span:nth-child(1)').text

# Extracting total number of pages from the text through regular expression
numbers = int(re.findall(r'\d+', total_number_page)[0])
total_page = math.ceil(numbers / 40)
print(total_page)

# Loop through each page
for page_no in range(1,total_page+1):
    driver.get(f"https://www.daraz.com.bd/routers/?page={page_no}")
    time.sleep(5)  # Wait for the page to load

    # List to store product links for the current page
    product_links = []
    
    # Loop through the products on the current page
    for prod in range(1,41):
        type_i = str(prod)
        link = driver.find_element(
            By.CSS_SELECTOR,f'#root > div > div.ant-row.FrEdP.css-1bkhbmc.app > div:nth-child(1) > div > div.ant-col.ant-col-20.ant-col-push-4.Jv5R8.css-1bkhbmc.app > div._17mcb > div:nth-child({type_i}) > div > div > div.ICdUp > div > a').get_attribute('href')
        product_links.append(link)

    # Add the current page's product links to the dictionary
    save_dict[f"page_{page_no}"] = product_links

# This is one of the main task of the assignment to print the dictionary with page no and links each respectively
for page, links in save_dict.items():
    print(f"{page}: {', '.join(links)}")

# Print the total number of products scraped
total_links = sum(len(links) for links in save_dict.values())
print(f"Total products scraped: {total_links}")

time.sleep(30)
driver.quit()
