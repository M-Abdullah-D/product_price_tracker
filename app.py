import pandas as pd
from paths import webdriver_path, browser_path, profile_path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import traceback, os
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Adding the domain and the category pages to be scraped
domain="https://www.amazon.com"
book_shelf="Best-Sellers-Books-Business-Development-Entrepreneurship/zgbs/books/2741"
website=f"{domain}/{book_shelf}/?_encoding=UTF8&language=en_US&currency=USD"

# Driver options
options = webdriver.ChromeOptions()
options.binary_location = browser_path
use_temp_profile = True
# When using a temporary profile, create a TemporaryDirectory object
# and pass its path to the browser; cleanup it up later.
temp_profile_dir = None
if use_temp_profile:
    import tempfile
    temp_profile_dir = tempfile.TemporaryDirectory(prefix="brave_profile_")
    options.add_argument(f"--user-data-dir={temp_profile_dir.name}")
else:
    options.add_argument(f"--user-data-dir={profile_path}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")      # Uncomment this after we make sure the code is working, this will run the browser in headless mode

service configuration and error handling
logpath = 'chromedriver_test.log'
service = Service(webdriver_path, log_path=logpath)
try:
    driver = webdriver.Chrome(service=service, options=options)
    logging.info("WebDriver initialized successfully.")
except Exception:
    traceback.print_exc()
    if os.path.exists(logpath):
        print('\n=== chromedriver log ===')
        with open(logpath) as f:
            print(open(logpath).read()[-2000:])
    # Clean up temporary profile if Chrome failed to start
    if temp_profile_dir is not None:
        try:
            temp_profile_dir.cleanup()
        except Exception:
            # Log cleanup failures so environment / filesystem issues are visible
            logging.info("Failed to clean up temporary Chrome profile directory:")
            traceback.print_exc()
    raise

# The lists of the books data:
Title_list = []
Author_list = []
Reviews_Rate_list = []
Reviews_Number_list = []
Kindle_price_list = []
Audiobook_price_list = []
Hardcover_price_list = []
Paperback_price_list = []
books_URLs = []

# Navigate to the website
# driver.get(website)
# logging.info(f"Successfully navigated to {website}")
# # Pagination
# pagination = driver.find_element(By.XPATH, '//*[contains(@class,"a-pagination")]')
# pages = pagination.find_elements(By.XPATH, "./li")
# last_page = int(pages[-2].text)
# current_page = 1

# while current_page <= last_page:
#     try:
#         driver.get(website)
#         logging.info(f"Successfully navigated to page {current_page}")

    # # Click the currency change element
    #     if current_page == 1:  # Change currency only on the first page to avoid unnecessary clicks
    #         try:
    #             sleep(3)  # Wait for the page to stabilize before clicking
    #             currency_list_element = WebDriverWait(driver, 3).until(
    #                 EC.element_to_be_clickable((By.XPATH, '//*[@id="icp-nav-flyout"]/button'))
    #             )
    #             currency_list_element.click()
    #             currency_element = WebDriverWait(driver, 10).until(
    #                 EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-flyout-icp"]/div[2]/ul[2]/li[2]/a'))
    #             )
    #             currency_element.click()
    #             logging.info("Currency changed successfully.")
    #             sleep(2)  # Wait for the currency change to complete
    #         except Exception:
    #             logging.info("Failed to change currency.")
    #             traceback.print_exc()

    # # add scrolling to the end of the list to load all content
    #     try:
    #         element = driver.find_element(By.XPATH, '//*[@id="endOfList"]')
    #         driver.execute_script("arguments[0].scrollIntoView();", element)
    #         logging.info("Page loaded successfully after scrolling.")
    #     except Exception:
    #         logging.info("Failed to load the page after scrolling.")
    #         traceback.print_exc()

    # Extract book pages URLs
    #     sleep(2)  # Wait for the book list to load after currency change
    #     books = driver.find_elements(By.XPATH, '//*[contains(@class,"zg-no-numbers")]')
    #     logging.info(f"Found {len(books)} books on the page.")
    #     for book in books: 
    #         try:
    #             URL = book.find_element(By.XPATH, './/span/div/div/div/div[2]/span/div/div/div/a').get_attribute('href')
    #             books_URLs.append(URL)
    #         except Exception:
    #             logging.info("Failed to extract book information.")
    #             traceback.print_exc()
    #     logging.info(f"Extracted URLs: {len(books_URLs)}")
    # # Going to the next page
    #     current_page+=1
    #     try:
    #         next_page=driver.find_element(By.XPATH, '//*[@id="CardInstanceTJXUd2yD4hIsSwroLLmNtw"]/div[2]/nav/ul/li[4]')
    #         next_page.click()
    #     except Exception:
    #         logging.info("Last page reached")
    # except Exception:
    #     logging.info(f"Failed to navigate to {website}")
    #     traceback.print_exc()




# Start navigating to the book pages and extract the required data
for url in books_URLs:  
    try:
        driver.get(url)
        # try:
        #     sleep(2)  # Wait for the page to load
        #     title_element = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, '//*[@id="productTitle"]'))
        #     )
        #     title = title_element.text
        #     Title_list.append(title)
        #     logging.info(f"Successfully navigated to the {books_URLs.index(url)+1} book: {title}")
        # except Exception:
        #     logging.info(f"Failed to navigate to the {books_URLs.index(url)+1} book.")
        #     traceback.print_exc()
        #     Title_list.append("X")

# Extract the author name
        # try:
        #     Author_element = driver.find_element(By.XPATH, '//*[@id="bylineInfo"]/span[1]/a')
        #     Author = Author_element.text
        #     Author_list.append(Author)
        #     logging.info("Successfully extracted the author name.")
        # except Exception:
        #     logging.info("Failed to extract the author name.")
        #     Author_list.append("X")
    
# The Reviews Section:
        # try:
        #     Reviews_Rate_element = driver.find_element(By.XPATH, '//*[@id="acrPopover"]/span/a/span')
        #     Reviews_Rate = Reviews_Rate_element.text
        #     Reviews_Rate_list.append(Reviews_Rate)
        #     Reviews_Number_element = driver.find_element(By.XPATH, '//*[@id="acrCustomerReviewText"]')
        #     Reviews_Number = Reviews_Number_element.text
        #     Reviews_Number_list.append(Reviews_Number)
        #     logging.info("Successfully extracted the reviews information.")
        # except Exception:
        #     logging.info("Failed to extract the reviews information.")
        #     Reviews_Rate_list.append("X")
        #     Reviews_Number_list.append("X")


# The Price Section:
        # Check if the Kindle version is available and add its price to the list
        # try:
        #     kindle_= driver.find_element(By.XPATH, '//*[@id="a-autoid-0-announce"]/span[1]/span')
        #     if kindle_.text == "Kindle":
        #         Kindle_price_element = driver.find_element(By.XPATH, '//*[@id="a-autoid-0-announce"]/span[2]/span')
        #         Kindle_price = Kindle_price_element.text
        #         Kindle_price_list.append(Kindle_price)
        #         logging.info("Successfully extracted the Kindle price.")
        #     else:
        #         logging.info("Kindle version not available.")
        #         Kindle_price_list.append("X")
        # except Exception:
        #     logging.info("Kindle version not available.")
        #     Kindle_price_list.append("X")
        # Check if the Audiobook version is available and add its price to the list
        # try:
        #     audiobook_ = driver.find_element(By.XPATH, '//*[@id="a-autoid-1-announce"]/span[1]/span')
        #     if audiobook_.text == "Audiobook":
        #         Audiobook_price_element = driver.find_element(By.XPATH, '//*[@id="a-autoid-1-announce"]/span[2]/span')
        #         Audiobook_price = Audiobook_price_element.text
        #         Audiobook_price_list.append(Audiobook_price)
        #         logging.info("Successfully extracted the Audiobook price.")
        #     else:
        #         logging.info("Audiobook version not available.")
        #         Audiobook_price_list.append("X")
        # except Exception:
        #     logging.info("Audiobook version not available.")
        #     Audiobook_price_list.append("X")
        # Check if the Hardcover version is available and add its price to the list
        # try:
        #     hardcover_ = driver.find_element(By.XPATH, '//*[@id="a-autoid-2-announce"]/span[1]/span')
        #     if hardcover_.text == "Hardcover":
        #         Hardcover_price_element = driver.find_element(By.XPATH, '//*[@id="a-autoid-2-announce"]/span[2]/span')
        #         Hardcover_price = Hardcover_price_element.text
        #         Hardcover_price_list.append(Hardcover_price)
        #         logging.info("Successfully extracted the Hardcover price.")
        #     else:
        #         logging.info("Hardcover version not available.")
        #         Hardcover_price_list.append("X")
        # except Exception:
        #     logging.info("Hardcover version not available.")
        #     Hardcover_price_list.append("X")
        # Check if the Paperback version is available and add its price to the list
        # try:
        #     paperback_ = driver.find_element(By.XPATH, '//*[@id="a-autoid-3-announce"]/span[1]/span')
        #     if paperback_.text == "Paperback":
        #         Paperback_price_element = driver.find_element(By.XPATH, '//*[@id="a-autoid-3-announce"]/span[2]/span')
        #         Paperback_price = Paperback_price_element.text
        #         Paperback_price_list.append(Paperback_price)
        #         logging.info("Successfully extracted the Paperback price.")
        #     else:
        #         logging.info("Paperback version not available.")
        #         Paperback_price_list.append("X")
        # except Exception:                    
        #     logging.info("Paperback version not available.")
        #     Paperback_price_list.append("X")

        
    except Exception:
        logging.info(f"Failed to extract price information for URL: {url}")
        traceback.print_exc()



# Close the browser and clean up the temporary profile
try:
    driver.quit()
except Exception:
    pass
finally:
    if temp_profile_dir is not None:
        try:
            temp_profile_dir.cleanup()
        except Exception:
            pass

print(f"Title:{len(Title_list)}, Author:{len(Author_list)}, Reviews_Rate:{len(Reviews_Rate_list)}, Reviews_Number:{len(Reviews_Number_list)}, Kindle_Price:{len(Kindle_price_list)}, Audiobook_Price:{len(Audiobook_price_list)}, Hardcover_Price:{len(Hardcover_price_list)}, Paperback_Price:{len(Paperback_price_list)}")

# df = pd.DataFrame({
#     "Title": Title_list,
#     "Author": Author_list,
#     "Reviews_Rate": Reviews_Rate_list,
#     "Reviews_Number": Reviews_Number_list,
#     "Kindle_Price": Kindle_price_list,
#     "Audiobook_Price": Audiobook_price_list,
#     "Hardcover_Price": Hardcover_price_list,
#     "Paperback_Price": Paperback_price_list
# })
# logging.info("DataFrame created successfully.")
# df.to_csv("books_data.csv", index=False)
# logging.info("Data saved to books_data.csv successfully.")
# Notes
