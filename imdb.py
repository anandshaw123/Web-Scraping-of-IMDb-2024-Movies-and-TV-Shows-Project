## Extracted the data and save into HTML file//

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

gecko_driver_path = "C://Users//anand//Desktop//imdb//geckodriver-v0.35.0-win32//geckodriver.exe"
firefox_binary_path = "C://Program Files//Mozilla Firefox//firefox.exe"


options = Options()
options.binary_location = firefox_binary_path

service = Service(gecko_driver_path)

driver = webdriver.Firefox(service=service, options=options)

driver.get('https://www.imdb.com/search/title/?release_date=2024-01-01,2024-12-31')

wait = WebDriverWait(driver, 10)
max_clicks = 2410617 ## Total Page

Unique_Links = set()


for _ in range(max_clicks):
    try:
        # Wait until the button is present
        button = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ipc-see-more')]/button")))

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        time.sleep(2) 

        # Ensure the button is clickable
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ipc-see-more')]/button")))

        driver.execute_script("arguments[0].click();", button)

        time.sleep(1) 

        num = 0

        elements = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")

        for element in elements:
            # Find and save links into TXT file
            try:
                link = element.find_element(By.TAG_NAME, "a")
                href = link.get_attribute("href")
                clean_link = href.split("?")[0]  
                if clean_link not in Unique_Links:  
                    Unique_Links.add(clean_link)

                    with open(f"Links/Extracted_{num}.txt", "w", encoding="utf-8") as f:
                        f.write(clean_link)

            except Exception as obj:
                print(f"Link Extraction Error OMG: {obj}")


            num += 1

        time.sleep(3) 
    
    except Exception as e:
        print(f"Error Brother OMG: {e}")
        break

time.sleep(30) 
driver.quit()



