# https://www.imdb.com/search/title/?release_date=2024-01-01,2024-12-31


# https://www.scraperapi.com/web-scraping/selenium/

# https://youtu.be/XI5_nsClCYI?si=wCmvniZNhkctKNGn


## ~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~~_~_~_~_~__~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~__~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~


##SMOOTH SCROLLING KE LIYE
    # button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ipc-title__wrapper']//h3[contains(@class, 'ipc-title__text')]/span[text()='Details']")))

    # # Smooth Scroll using JavaScript Loop
    # for i in range(0, 100, 5):  # धीरे-धीरे स्क्रॉल करने के लिए
    #     driver.execute_script(f"window.scrollBy(0, {i});")
    #     time.sleep(0.05)  # थोड़ा इंतजार ताकि स्मूथ इफेक्ट आए

    # time.sleep(2)  # कुछ सेकंड रुकें

    # # Scroll directly to the element
    # driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
    # time.sleep(3) 


##~_~_~_~_~__~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~~_~_~_~_~__~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~__~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~__~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~

## Extracted the data and save into HTML file//

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# GeckoDriver और Firefox का सही path
gecko_driver_path = "C://Users//anand//Desktop//imdb//geckodriver-v0.35.0-win32//geckodriver.exe"
firefox_binary_path = "C://Program Files//Mozilla Firefox//firefox.exe"

# Firefox options सेट करें
options = Options()
options.binary_location = firefox_binary_path

# GeckoDriver सर्विस सेट करें
service = Service(gecko_driver_path)

# WebDriver इनिशियलाइज़ करें
driver = webdriver.Firefox(service=service, options=options)

# IMDb Page Open Karein
driver.get('https://www.imdb.com/search/title/?release_date=2024-01-01,2024-12-31')

# WebDriverWait define करें
wait = WebDriverWait(driver, 10)
max_clicks = 2410617 ## Total Page

# यूनिक लिंक स्टोर करने के लिए सेट
Unique_Links = set()


for _ in range(max_clicks):
    try:
        # Wait until the button is present
        button = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ipc-see-more')]/button")))

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        time.sleep(2)  # स्क्रॉल सेटल होने के लिए

        # Ensure the button is clickable
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ipc-see-more')]/button")))

        # Click using JavaScript to avoid out-of-bounds issue
        driver.execute_script("arguments[0].click();", button)

        time.sleep(1)  # **1 सेकंड वेट करने के बाद डेटा एक्सट्रैक्ट करना स्टार्ट करेंगे**

        # Data Extraction
        file = 0
        num = 0

        elements = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")

        for element in elements:
            # HTML extract & save
            htmls = element.get_attribute("outerHTML")
            with open(f"data/Extracted_{file}.html", "w", encoding="utf-8") as f:
                f.write(htmls)



            # Find and save links into CSV/Excel File.
            # try:
            #     link = element.find_element(By.TAG_NAME, "a")
            #     href = link.get_attribute("href")
            #     clean_link = href.split("?")[0]### '?' के बाद का हिस्सा हटाना
            #     if clean_link not in Unique_Links: ### सिर्फ यूनिक लिंक स्टोर करना
            #         Unique_Links.add(clean_link)

            # except Exception as obj:
            #     print(f"Link Extraction Error OMG: {obj}")



            # Find and save links into TXT file
            try:
                link = element.find_element(By.TAG_NAME, "a")
                href = link.get_attribute("href")
                clean_link = href.split("?")[0]  # '?' के बाद का हिस्सा हटाना
                if clean_link not in Unique_Links:  # सिर्फ यूनिक लिंक स्टोर करना
                    Unique_Links.add(clean_link)

                    # लिंक को फ़ाइल में सेव करें
                    with open(f"Links/Extracted_{num}.txt", "w", encoding="utf-8") as f:
                        f.write(clean_link)

            except Exception as obj:
                print(f"Link Extraction Error OMG: {obj}")


            file += 1
            num += 1

        time.sleep(3)  #5 sec **Next क्लिक से पहले वेट करें ताकि नया डेटा लोड हो** 
    
    except Exception as e:
        print(f"Error Brother OMG: {e}")
        break

time.sleep(30)  # **एंड में 30 सेकंड वेट करने के लिए**
driver.quit()

df = pd.DataFrame({"Links": list(Unique_Links)})
df.to_csv("Links.csv", index=False, encoding="utf-8")
























































































































## Only extracing data and save into html file No Scrolling and clicking
# import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service


# chrome_driver_path = "C://Users//anand//Desktop//Web Scraping of The most popular shows to watch//chromedriver-win64//chromedriver.exe"

# service = Service(chrome_driver_path)

# driver = webdriver.Chrome(service=service)
# driver.get('https://www.imdb.com/search/title/?release_date=2024-01-01,2024-12-31')
# Maximize window
# driver.maximize_window()
































































### ~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~_~__~_~_~_~_~_~_~_~_~_~_~_~_____~_~_~_~_~___~_~_~_~_~__~_~_~__~_~_~~__~_~_~_~_~_~_


### Only Extracted Outer HTML file and scrolling and clicking Codes


# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager



# gecko_driver_path = "C://Users//anand//Desktop//imdb//geckodriver-v0.35.0-win32//geckodriver.exe"
# # Path to the Firefox browser binary
# firefox_binary_path = "C://Program Files//Mozilla Firefox//firefox.exe"  # Update this with the correct path

# # Set up the Firefox options to specify the binary location
# options = Options()
# options.binary_location = firefox_binary_path

# # Set up the service object for GeckoDriver
# service = Service(gecko_driver_path)

# # Initialize Firefox WebDriver with the service object and options
# driver = webdriver.Firefox(service=service, options=options)

# # IMDb Page Open Karein
# driver.get('https://www.imdb.com/search/title/?release_date=2024-01-01,2024-12-31')


# file = 0
# elements = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")
# for element in elements:
#     htmls = element.get_attribute("outerHTML")
#     with open (f"data/Extracted_{file}.html", "w",encoding="utf-8") as f:
#         f.write(htmls)
#         file += 1

# time.sleep(30)
# driver.close()





























# # ##-------------------------------------------------------Ye Sirf Scrolling and Clicking ke liye hai ----------------------------------------------------------------------------

# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# # Correct path to the GeckoDriver (for Firefox)
# gecko_driver_path = "C://Users//anand//Desktop//imdb//geckodriver-v0.35.0-win32//geckodriver.exe"

# # Path to the Firefox browser binary
# firefox_binary_path = "C://Program Files//Mozilla Firefox//firefox.exe" 

# # Set up the Firefox options to specify the binary location
# options = Options()
# options.binary_location = firefox_binary_path

# # Set up the service object for GeckoDriver
# service = Service(gecko_driver_path)

# # Initialize Firefox WebDriver with the service object and options
# driver = webdriver.Firefox(service=service, options=options)

# # IMDb Page Open Karein
# driver.get('https://www.imdb.com/search/title/?release_date=2024-01-01,2024-12-31')

# # Define WebDriverWait
# wait = WebDriverWait(driver, 10)
# max_clicks = 10

# for _ in range(max_clicks):
#     try:
#         # Wait until the button is present
#         button = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ipc-see-more')]/button")))

#         # Scroll into view
#         driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
#         time.sleep(2)  # Scroll settle hone ka wait karein

#         # Ensure the button is clickable
#         wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ipc-see-more')]/button")))

#         # Click using JavaScript to avoid out-of-bounds issue
#         driver.execute_script("arguments[0].click();", button)

#         time.sleep(1)  # Wait for content to load
#     except Exception as e:
#         print(f"Hyee , error occurred Brother!!: {e}")
#         break
    
# driver.quit()

















































# ######################################################### Extracted Only data HTML format files

# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# # GeckoDriver और Firefox का सही path
# gecko_driver_path = "C://Users//anand//Desktop//imdb//geckodriver-v0.35.0-win32//geckodriver.exe"
# firefox_binary_path = "C://Program Files//Mozilla Firefox//firefox.exe"

# # Firefox options सेट करें
# options = Options()
# options.binary_location = firefox_binary_path

# # GeckoDriver सर्विस सेट करें
# service = Service(gecko_driver_path)

# # WebDriver इनिशियलाइज़ करें
# driver = webdriver.Firefox(service=service, options=options)

# # IMDb Page Open Karein
# driver.get('https://www.imdb.com/search/title/?release_date=2024-01-01,2024-12-31')

# # WebDriverWait define करें
# wait = WebDriverWait(driver, 10)
# max_clicks = 6


# for _ in range(max_clicks):
#     try:
#         # Wait until the button is present
#         button = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ipc-see-more')]/button")))

#         # Scroll into view
#         driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
#         time.sleep(2)  # स्क्रॉल सेटल होने के लिए

#         # Ensure the button is clickable
#         wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ipc-see-more')]/button")))

#         # Click using JavaScript to avoid out-of-bounds issue
#         driver.execute_script("arguments[0].click();", button)

#         time.sleep(3)  # **3 सेकंड वेट करने के बाद डेटा एक्सट्रैक्ट करना स्टार्ट करेंगे**

#         # Data Extraction
#         file = 0
#         elements = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item") # Each Box ke element ko diya gaya hai 
#         for element in elements:
#             htmls = element.get_attribute("outerHTML")
#             with open(f"data/Extracted_{file}.html", "w", encoding="utf-8") as f:
#                 f.write(htmls)
#             file += 1

#         time.sleep(5)  # **Next क्लिक से पहले वेट करें ताकि नया डेटा लोड हो**
    
#     except Exception as e:
#         print(f"Error: {e}")
#         break

# time.sleep(40)  # **एंड में 40 सेकंड वेट करने के लिए**
# driver.quit()




































##---------------------------------------------------------- Extracting the Multiple links test.py
# import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service

# chrome_driver_path = "C://Users//anand//Desktop//Web Scraping of The most popular shows to watch//chromedriver-win64//chromedriver.exe"

# service = Service(chrome_driver_path)

# driver = webdriver.Chrome(service=service)

# driver.get('https://www.imdb.com/search/title/?release_date=2024-01-01,2024-12-31')




## Extracting Only Links 

# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager



# # Correct path to the GeckoDriver (for Firefox)
# gecko_driver_path = "C://Users//anand//Desktop//imdb//geckodriver-v0.35.0-win32//geckodriver.exe"

# # Path to the Firefox browser binary
# firefox_binary_path = "C://Program Files//Mozilla Firefox//firefox.exe"  # Update this with the correct path

# # Set up the Firefox options to specify the binary location
# options = Options()
# options.binary_location = firefox_binary_path

# # Set up the service object for GeckoDriver
# service = Service(gecko_driver_path)

# # Initialize Firefox WebDriver with the service object and options
# driver = webdriver.Firefox(service=service, options=options)

# # IMDb Page Open Karein
# driver.get('https://www.imdb.com/search/title/?release_date=2024-01-01,2024-12-31')


# elements = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")

# for element in elements:

#     # Find the <a> tag inside each element
#     link = element.find_element(By.TAG_NAME, "a")
#     href = link.get_attribute("href")  # Extract the href attribute
#     print(href)

# time.sleep(2)
# driver.close()









# Joining the links------------------------------------------------------Code Only..

# from urllib.parse import urljoin

# base_url = "https://www.imdb.com"  # Set the base URL of the website
# full_link = urljoin(base_url, link)
# print(full_link)  # Output: https://www.imdb.com/title/tt5040012/?ref_=sr_t_1









# KPI stands for Key Performance Indicator. It is a measurable value that shows how effectively a person, team, or organization is achieving a specific goal.

# Examples:

# For a website: Number of monthly visitors
# For a sales team: Total sales made in a month
# For customer support: Average time taken to resolve an issue