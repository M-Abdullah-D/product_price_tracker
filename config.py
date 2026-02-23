from selenium import webdriver
from dotenv import load_dotenv
import os
import tempfile




__all__ = ["domain", "book_shelf", "website", "options", "XPATHS"]

# Adding the domain and the category pages to be scraped
domain="https://www.amazon.com"
book_shelf="Best-Sellers-Books-Business-Development-Entrepreneurship/zgbs/books/2741"
website=f"{domain}/{book_shelf}/?_encoding=UTF8&language=en_US&currency=USD"



# Driver options
load_dotenv()
options = webdriver.ChromeOptions()
use_temp_profile = True
if use_temp_profile:
    required = ["BROWSER_PATH"]
else:
    required = ["BROWSER_PATH", "CHROME_PROFILE_PATH"]
if missing:= [var for var in required if not os.getenv(var)]:
    raise ValueError(f"Missing required environment variables: {missing}")

options.binary_location = os.getenv('BROWSER_PATH')

# When using a temporary profile, create a TemporaryDirectory object
# and pass its path to the browser; cleanup it up later.
temp_profile_dir = None
if use_temp_profile:
    temp_profile_dir = tempfile.TemporaryDirectory(prefix="brave_profile_")
    options.add_argument(f"--user-data-dir={temp_profile_dir.name}")
else:
    options.add_argument(f"--user-data-dir={os.getenv('CHROME_PROFILE_PATH')}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")      # Uncomment this after we make sure the code is working, this will run the browser in headless mode





XPATHS = {
    "pagination": '//*[contains(@class,"a-pagination")]',
    "pages": './li',
    "currency_list": '//*[@id="icp-nav-flyout"]/button',
    "currency_element": '//*[@id="nav-flyout-icp"]/div[2]/ul[2]/li[2]/a',
    "end_of_page": '//*[@id="endOfList"]',
    "books": '//*[contains(@class,"zg-no-numbers")]',
    "URL":'.//span/div/div/div/div[2]/span/div/div/div/a',
    "next_page": '//*[contains(@class,"a-last")]',
    "title_element": '//*[@id="productTitle"]',
    "Author_element": '//*[@id="bylineInfo"]/span[1]/a',
    "Reviews_Rate_element":'//*[@id="acrPopover"]/span/a/span',
    "Reviews_Number_element":'//*[@id="acrCustomerReviewText"]',
    "Kindle":'//*[@id="a-autoid-0-announce"]/span[1]/span',
    "Kindle_price_element":'//*[@id="a-autoid-0-announce"]/span[2]/span',
    "Audiobook":'//*[@id="a-autoid-1-announce"]/span[1]/span',
    "Audiobook_price_element":'//*[@id="a-autoid-1-announce"]/span[2]/span',
    "Paperback":'//*[@id="a-autoid-3-announce"]/span[1]/span',
    "Paperback_price_element":'//*[@id="a-autoid-3-announce"]/span[2]/span',
    "Hardcover":'//*[@id="a-autoid-2-announce"]/span[1]/span',
    "Hardcover_price_element":'//*[@id="a-autoid-2-announce"]/span[2]/span'
}