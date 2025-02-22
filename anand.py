import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Lists to store scraped data
names_list = []
Rating = []
total_votes = []
storyline = []
overview = []
Castings = []
release_dates_list = []
revenue = []
Budget = []
movie_links = []
genres = []
language = []
tagline = []
production_company = []
runtime = []

## Read all links from "Links" folder (Sorted numerically)
files = os.listdir("oldone")
files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

linkss = []
for filename in files:
    file_path = os.path.join("oldone", filename)
    with open(file_path, encoding="utf-8") as file:
        link = file.read().strip()
        clean_link = link.split("?")[0]
        linkss.append(clean_link)

# GeckoDriver and Firefox paths
gecko_driver_path = "C://Users//anand//Desktop//imdb//geckodriver-v0.35.0-win32//geckodriver.exe"
firefox_binary_path = "C://Program Files//Mozilla Firefox//firefox.exe"

# Set Firefox options
options = Options()
options.binary_location = firefox_binary_path

# Initialize WebDriver
service = Service(gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

# IMDb Scraping
for Linkss in linkss:
    driver.get(Linkss)
    wait = WebDriverWait(driver, 2)


    try:
        # Save Movie Link
        movie_links.append(Linkss)

        # # Extract Movie Name
        name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.hero__primary-text[data-testid="hero__primary-text"]')))
        print("Movie Name:", name.text)
        names_list.append(name.text)

        # Extract Overview
        try:
            ov = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[role="presentation"][data-testid="plot-xl"]')))
            print("Overview:",ov.text)
            overview.append(ov.text if ov else "Not_Present")
        except:
            overview.append("Not_Found")

        # Extract Average Ratings
        try:
            rating = driver.find_element(By.XPATH, '//div[@data-testid="hero-rating-bar__aggregate-rating"]//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[1]')
            print("Average Ratings:",rating.text)
            Rating.append(rating.text if rating else "00")
            
        except:
            Rating.append("00")

        # Extract Total Votes
        try:
            total_v = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='hero-rating-bar__aggregate-rating']//div[contains(@class, 'sc-d541859f-3')]")))
            print("Total Votes:",total_v.text)
            total_votes.append(total_v.text if total_v else "00")
        except:
            total_votes.append("00")

        # Extract Cast (FIXED)
        try:
            casted = wait.until(EC.presence_of_element_located((By.XPATH, '//h3[@class="ipc-title__text"]/span[text()="Top cast"]')))
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", casted)
            time.sleep(2)
            Cast = driver.find_elements(By.CSS_SELECTOR, "a.sc-cd7dc4b7-1.kVdWAO")
            print("Cast:",[casting.text for casting in Cast] if Cast else ["Not_Found"])
            Castings.append([casting.text for casting in Cast] if Cast else ["Not_Found"])
        except:
            Castings.append(["Not_Found"])

        # Extract Storyline
        try:
            SL = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[@class='ipc-title__text']/span[text()='Storyline']")))
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", SL)
            time.sleep(2)
            storyline_text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='storyline-plot-summary']//div[@class='ipc-html-content-inner-div']")))
            print("Storyline:",storyline_text.text)
            storyline.append(storyline_text.text if storyline_text.text else "Not_Found")
        except:
            storyline.append("Not_Found")

        # Extract Tagline
        try:
            tag_l = wait.until(EC.presence_of_element_located((By.XPATH, "//li[@data-testid='storyline-taglines']//span[@class='ipc-metadata-list-item__list-content-item']")))
            print("Tagline:",tag_l.text)
            tagline.append(tag_l.text if tag_l.text else "Not_Found")
        except:
            tagline.append("Not_Found")

        # Extract Genres
        try:
            genres_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-testid='storyline-genres']//a")))
            print("Genres:",[genre.text for genre in genres_elements] if genres_elements else ["Not_found"])
            genres.append([genre.text for genre in genres_elements] if genres_elements else ["Not_found"])
        except:
            genres.append(["Not_Found"])

        # # Extract Release Dates (FIXED)
        try:
            button = wait.until(EC.presence_of_element_located((By.XPATH, "//h3/span[text()='Details']")))
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
            time.sleep(2)
            release_dates = driver.find_elements(By.XPATH, "//a[contains(@href, 'releaseinfo')]")
            print("Release Dates",[release.text.strip() for release in release_dates if ',' in release.text] if release_dates else ["Not_Found"])
            release_dates_list.append([release.text.strip() for release in release_dates if ',' in release.text] if release_dates else ["Not_Found"])
        except:
            release_dates_list.append(["Not_Found"])

        # Extract Languages
        try:
            languages_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-testid='title-details-languages']//a")))
            print("Languages:",[lang.text for lang in languages_elements] if languages_elements else ["Not_Found"])
            language.append([lang.text for lang in languages_elements] if languages_elements else ["Not_Found"])
        except:
            language.append(["Not_Found"])


        # Extract Production Company
        try:
            company_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-testid='title-details-companies']//a[@class='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link']")))
            print("Production_Company:",[company.text for company in company_elements] if company_elements else ["Not_Found"])
            production_company.append([company.text for company in company_elements] if company_elements else ["Not_Found"])
        except:
            production_company.append(["Not_Found"])

        # Extract Budget
        try:
            for_budget = wait.until(EC.presence_of_element_located((By.XPATH, '//h3[@class="ipc-title__text"]/span[text()="Box office"]')))
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", for_budget)
            time.sleep(1)
            budget_element = driver.find_element(By.XPATH, "//li[@data-testid='title-boxoffice-budget']//span[@class='ipc-metadata-list-item__list-content-item']")
            print("Budget:", budget_element.text)
            Budget.append(budget_element.text.split(' ')[0] if budget_element else "000")
        except:
            Budget.append("000")

        try:
            Rev_e = driver.find_element(By.XPATH, '//li[@data-testid="title-boxoffice-cumulativeworldwidegross"]//span[@class="ipc-metadata-list-item__list-content-item"]')
            print("Revenues:", Rev_e.text if Rev_e else "000")
            revenue.append(Rev_e.text if Rev_e.text else "000")
        except:
            revenue.append("000")

        # Extract Runtime
        try:
            RNT = wait.until(EC.presence_of_element_located((By.XPATH, "//a/h3/span[text()='Tech specs']")))
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", RNT)
            time.sleep(1)
            Run_t = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-testid='title-techspec_runtime']//div")))
            print("RunTime:",[i.text for i in Run_t] if Run_t else ["Not_found"])
            runtime.append([i.text for i in Run_t] if Run_t else ["Not_found"])
        except:
            runtime.append(["Not_Found"])

    except Exception as e:
        print(f"Error on {link}: {e}")

# Close driver
driver.quit()

# Save to DataFrame and CSV
df = pd.DataFrame({
    "Budget": Budget,
    "Home_Page": movie_links,
    "Movie_Name": names_list,
    "Genres": genres,
    "Overview": overview,
    "Cast": Castings,
    "Original_Language":language,
    "Storyline": storyline,
    "Production_Company":production_company,
    "Release_Date": release_dates_list,
    "Revenue": revenue,
    "Run_Time": runtime,
    "Tagline":tagline,
    "Vote_Average":Rating,
    "Vote_Count":total_votes
})

df.to_csv("IMDb 2024 Movies TV Shows.csv", index=False, encoding="utf-8")

























































































# ### Es code mein Real Xpth used kiya gaya hai jo anand.py mein hai Code GPT ka hai


# import os
# import time
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Lists to store scraped data
# names_list = []
# Rating = []
# total_votes = []
# storyline = []
# overview = []
# Castings = []
# release_dates_list = []
# Budget = []
# movie_links = []
# genres = []
# language = []
# tagline = []
# production_company = []
# runtime = []

# # Read all links from "Links" folder
# linkss = []
# for links in os.listdir("Links"):
#     with open(f"Links/{links}", encoding="utf-8") as l:
#         linkss.append(l.read().strip())

# # GeckoDriver and Firefox paths
# gecko_driver_path = "C://Users//anand//Desktop//imdb//geckodriver-v0.35.0-win32//geckodriver.exe"
# firefox_binary_path = "C://Program Files//Mozilla Firefox//firefox.exe"

# # Set Firefox options
# options = Options()
# options.binary_location = firefox_binary_path
# # options.add_argument("--headless")  # Uncomment for headless mode

# # Initialize WebDriver
# service = Service(gecko_driver_path)
# driver = webdriver.Firefox(service=service, options=options)

# # IMDb Scraping
# for link in linkss:
#     driver.get(link)
#     wait = WebDriverWait(driver, 12)

#     try:
#         # Save Movie Link
#         movie_links.append(link)

#         # Extract Movie Name
#         name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.hero__primary-text[data-testid="hero__primary-text"]')))
#         print("Movie Name:", name.text)
#         names_list.append(name.text)

#         # Extract Overview
#         try:
#             ov = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[role="presentation"][data-testid="plot-xl"]')))
#             overview.append(ov.text if ov else "Not_Present")
#         except:
#             overview.append("Not_Found")

#         # Extract Average Ratings
#         try:
#             rating = driver.find_element(By.XPATH, '//div[@data-testid="hero-rating-bar__aggregate-rating"]//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[1]')
#             Rating.append(rating.text if rating else "00")
#         except:
#             Rating.append("00")

#         # Extract Total Votes
#         try:
#             total_v = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='hero-rating-bar__aggregate-rating']//div[contains(@class, 'sc-d541859f-3')]")))
#             total_votes.append(total_v.text if total_v else "00")
#         except:
#             total_votes.append("00")

#         # Extract Cast (FIXED)
#         try:
#             casted = wait.until(EC.presence_of_element_located((By.XPATH, '//h3[@class="ipc-title__text"]/span[text()="Top cast"]')))
#             driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", casted)
#             time.sleep(5)
#             Cast = driver.find_elements(By.CSS_SELECTOR, "a.sc-cd7dc4b7-1.kVdWAO")
#             Castings.append([casting.text for casting in Cast] if Cast else ["Not_Found"])
#         except:
#             Castings.append(["Not_Found"])

#         # Extract Storyline
#         try:
#             SL = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[@class='ipc-title__text']/span[text()='Storyline']")))
#             driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", SL)
#             time.sleep(5)
#             storyline_text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='storyline-plot-summary']//div[@class='ipc-html-content-inner-div']")))
#             storyline.append(storyline_text.text if storyline_text.text else "Not_Found")
#         except:
#             storyline.append("Not_Found")

#         # Extract Tagline
#         try:
#             tag_l = wait.until(EC.presence_of_element_located((By.XPATH, "//li[@data-testid='storyline-taglines']//span[@class='ipc-metadata-list-item__list-content-item']")))
#             tagline.append(tag_l.text if tag_l.text else "Not_Found")
#         except:
#             tagline.append("Not_Found")

#         # Extract Genres
#         try:
#             genres_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-testid='storyline-genres']//a[@class='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link']")))
#             genres.append([genre.text for genre in genres_elements] if genres_elements else ["Not_found"])
#         except:
#             genres.append(["Not_Found"])

#         # Extract Release Dates (FIXED)
#         try:
#             button = wait.until(EC.presence_of_element_located((By.XPATH, "//h3/span[text()='Details']")))
#             driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
#             time.sleep(2)
#             release_dates = driver.find_elements(By.XPATH, "//a[contains(@href, 'releaseinfo')]")
#             release_dates_list.append([release.text.strip() for release in release_dates if ',' in release.text] if release_dates else ["Not_Found"])
#         except:
#             release_dates_list.append(["Not_Found"])

#         # Extract Languages
#         try:
#             languages_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-testid='title-details-languages']//a[@class='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link']")))
#             language.append([lang.text for lang in languages_elements] if languages_elements else ["Not_Found"])
#         except:
#             language.append(["Not_Found"])

#         # Extract Production Company
#         try:
#             company_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-testid='title-details-companies']//a[@class='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link']")))
#             production_company.append([company.text for company in company_elements] if company_elements else ["Not_Found"])
#         except:
#             production_company.append(["Not_Found"])

#         # Extract Budget
#         try:
#             for_budget = wait.until(EC.presence_of_element_located((By.XPATH, '//h3/span[text()="Box office"]')))
#             driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", for_budget)
#             time.sleep(2)
#             budget_element = driver.find_element(By.XPATH, "//li[@data-testid='title-boxoffice-budget']//span[@class='ipc-metadata-list-item__list-content-item']")
#             Budget.append(budget_element.text.split()[0] if budget_element else "000")
#         except:
#             Budget.append("000")

#         # Extract Runtime
#         try:
#             RNT = wait.until(EC.presence_of_element_located((By.XPATH, "//a/h3/span[text()='Tech specs']")))
#             driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", RNT)
#             time.sleep(3)
#             Run_t = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-testid='title-techspec_runtime']//div[@class='ipc-metadata-list-item__content-container']")))
#             runtime.append([i.text for i in Run_t] if Run_t else ["Not_found"])
#         except:
#             runtime.append(["Not_Found"])

#     except Exception as e:
#         print(f"Error on {link}: {e}")

# # Close driver
# driver.quit()

# # Save to DataFrame and CSV
# df = pd.DataFrame({
#     "Budget": Budget,
#     "Home_Page": movie_links,
#     "Movie_Name": names_list,
#     "Genres": genres,
#     "Overview": overview,
#     "Cast": Castings,
#     "Original_Language": language,
#     "Storyline": storyline,
#     "Production_Company": production_company,
#     "Release_Date": release_dates_list,
#     "Run_Time": runtime,
#     "Tagline": tagline,
#     "Vote_Average": Rating,
#     "Vote_Count": total_votes
# })

# df.to_csv("IMDb_2024_Movies_TV_Shows.csv", index=False, encoding="utf-8")
















































































































































































































## OLD Code Hai:


# import os
# import time
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Lists to store scraped data
# names_list = []
# Rating = []
# total_votes = []
# storyline = []
# overview = []
# Castings = []
# release_dates_list = []
# Budget = []
# movie_links = []
# genres = []
# language = []
# tagline = []
# production_company = []
# runtime = []


# # Read all links from "Links" folder
# linkss = [] ## linkss = set()
# for links in os.listdir("Links"):
#     with open(f"Links/{links}", encoding="utf-8") as l:
#         linkss.append(l.read().strip()) ## If you used [add] function then its automatically removes duplicates links converted into python SET(Sets)

# # GeckoDriver और Firefox का सही path
# gecko_driver_path = "C://Users//anand//Desktop//imdb//geckodriver-v0.35.0-win32//geckodriver.exe"
# firefox_binary_path = "C://Program Files//Mozilla Firefox//firefox.exe"

# # Firefox options सेट करें
# options = Options()
# options.binary_location = firefox_binary_path
# # options.add_argument("--headless")  # Run without opening Firefox UI (optional)

# # GeckoDriver सर्विस सेट करें
# service = Service(gecko_driver_path)

# # WebDriver इनिशियलाइज़ करें (बाहर रखना ज़रूरी है)
# driver = webdriver.Firefox(service=service, options=options)

# ## IMDb Pages Open करके Data Scrap करें
# for link in linkss:
#     driver.get(link)
#     wait = WebDriverWait(driver, 12)

#     try:

#         # Save Movie Link
#         movie_links.append(link)



#         # Extract Movie Name
#         name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.hero__primary-text[data-testid="hero__primary-text"]')))
#         print("Movie Name:", name.text)
#         names_list.append(name.text)  # Store in list




#         try: ##Extract Overview
#             ov = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[role="presentation"][data-testid="plot-xl"]')))
#             overview.append(ov.text if ov else "Not_Present")
#             print(overview)
#         except:
#             overview.append("Not_Found")




#         ## Extract Average Ratings
#         rating = driver.find_element(By.XPATH, '//div[@data-testid="hero-rating-bar__aggregate-rating"]//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[1]')
#         print(rating.text)
#         Rating.append(rating.text if rating else "00")




#             ## Extract Total_votes
#         total_v = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='hero-rating-bar__aggregate-rating']//div[contains(@class, 'sc-d541859f-3')]")))
#         # print(rating.text)
#         print(total_v.text)
#         total_votes.append(total_v.text if total_v else "00")




#         # Extract Cast
#         casted = wait.until(EC.presence_of_element_located((By.XPATH, '//h3[@class="ipc-title__text"]/span[text()="Top cast"]')))
#         driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", casted)
#         time.sleep(10)
#         Cast = driver.find_elements(By.CSS_SELECTOR, "a.sc-cd7dc4b7-1.kVdWAO")
#         for casting in Cast:
#             print("Cast:", casting.text)
#             Castings.append(casting.text)



                    
#         try:## ##Extract StoryLine
#             SL = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[@class='ipc-title__text']/span[text()='Storyline']")))
#             driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", SL)
#             time.sleep(12)
#             storyline_text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='storyline-plot-summary']//div[@class='ipc-html-content-inner-div']")))
#             print(storyline)
#             storyline.append(storyline_text.text if storyline_text.text else "Not_Found")
#         except:
#             storyline.append("Not_Found")


#         try:
#             tag_l = wait.until(EC.presence_of_element_located((By.XPATH, "//li[@data-testid='storyline-taglines']//span[@class='ipc-metadata-list-item__list-content-item']")))
#             tagline.append(tag_l.text if tag_l.text else "Not_Found")
#             print(tagline)
#         except:
#             tagline.append("Not_Found")

#         try:
#             genres_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-testid='storyline-genres']//a[@class='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link']")))
#             genres.append([genre.text for genre in genres_elements] if genres_elements else ["Not_found"])
#         except:
#             genres.append("Not_Found")




#         ## Extract Release Dates
#         button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ipc-title__wrapper']//h3[contains(@class, 'ipc-title__text')]/span[text()='Details']")))
#         driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
#         time.sleep(3)
#         release_dates = driver.find_elements(By.XPATH, "//a[contains(@href, 'releaseinfo')]")
#         for release in release_dates:
#             date_text = release.text.strip()
#             if ',' in date_text:
#                 print("Release Date:", date_text)
#                 release_dates_list.append(date_text)



#         try:
#                                 ## Extracted language
#             languages_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-testid='title-details-languages']//a[@class='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link']")))
#             language.append([lang.text for lang in languages_elements] if languages_elements else ["Languages not found"])
#             print(languages_elements)
#         except:
#             language.append("Not_Found")



#         try: ##Extract production_company
#             company_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-testid='title-details-companies']//a[@class='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link']")))
#             production_company.append([company.text for company in company_elements] if company_elements else ["Not_Found"])
#         except:
#             production_company.append("Not_Found")




#         ## Extract Budget
#         for_budget = wait.until(EC.presence_of_element_located((By.XPATH, '//h3[@class="ipc-title__text"]/span[text()="Box office"]')))
#         driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", for_budget)
#         time.sleep(2)
#         budget_element = driver.find_element(By.XPATH, "//li[@data-testid='title-boxoffice-budget']//span[@class='ipc-metadata-list-item__list-content-item']")
#         print("Budget:", budget_element.text)
#         Budget.append(budget_element.text.split()[0] if budget_element else "000")


#         ## Extract Runtime
#         RNT = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='ipc-title-link-wrapper']/h3/span[text()='Tech specs']")))
#         driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", RNT)
#         time.sleep(3)
#         Run_t = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-testid='title-techspec_runtime']//div[@class='ipc-metadata-list-item__content-container']")))
#         runtime.append([i.text for i in Run_t] if Run_t else ["Not found"])

        



#     except Exception as e:
#         print(f"Error on {link}: {e}")

# # ड्राइवर बंद करें (बाहर रखना ज़रूरी है)
# driver.quit()




# df = pd.DataFrame({
#     "Budget": Budget,
#     "Home_Page": movie_links,
#     "Movie_Name": names_list,
#     "Genres": genres,
#     "Overview": overview,
#     "Cast": Castings,
#     "Original_Language":language,
#     "Storyline": storyline,
#     "Production_Company":production_company,
#     "Release_Date": release_dates_list,
#     "Run_Time": runtime,
#     "Tagline":tagline,
#     "Vote_Average":Rating,
#     "Vote_Count":total_votes
# })

# ##Save DataFrame as CSV
# df.to_csv("IMDb_2024_Movies_TV_Shows.csv", index=False, encoding="utf-8")

















# # https://www.imdb.com/title/tt5040012/?ref_=sr_i_1


# # #  ________________Casting ka xpath 
# # elements = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='title-cast-item__actor']")
# # for element in elements:
# #     print(element.text)








