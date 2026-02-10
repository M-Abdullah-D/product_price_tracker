from paths import webdriver_path, browser_path, profile_path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Adding the path to the webdriver and the browser
webdriver_path=webdriver_path
browser_path=browser_path
profile_path=profile_path

# Adding the domain and the category pages to be scraped
domain="https://www.amazon.com"
book_shelf="Best-Sellers-Books-Business-Development-Entrepreneurship/zgbs/books/2741"
page_num=["1","2"]
for page in page_num:
    website=f"{domain}/{book_shelf}/?_encoding=UTF8&pg={page}"

# Driver options
options = webdriver.ChromeOptions()
options.binary_location = browser_path
use_temp_profile = True
if use_temp_profile:
    import tempfile
    temp_prfile = tempfile.mkdtemp(prefix="brave_profile_")
    options.add_argument(f"--user-data-dir={temp_prfile}")
else:
    options.add_argument(f"--user-data-dir={profile_path}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless=new")      # Uncomment this after we make sure the code is working, this will run the browser in headless mode
logpath = 'chromedriver_test.log'
service = Service(webdriver_path, log_path=logpath)
