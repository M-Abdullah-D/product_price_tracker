from paths import webdriver_path, browser_path, profile_path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# Adding the domain and the category pages to be scraped
domain="https://www.amazon.com"
book_shelf="Best-Sellers-Books-Business-Development-Entrepreneurship/zgbs/books/2741"
website=f"{domain}/{book_shelf}/?_encoding=UTF8&pg=1"

# Driver options
options = webdriver.ChromeOptions()
options.binary_location = browser_path
use_temp_profile = True
if use_temp_profile:
    import tempfile
    temp_profile = tempfile.mkdtemp(prefix="brave_profile_")
    options.add_argument(f"--user-data-dir={temp_profile}")
else:
    options.add_argument(f"--user-data-dir={profile_path}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless=new")      # Uncomment this after we make sure the code is working, this will run the browser in headless mode

# service configuration and error handling
logpath = 'chromedriver_test.log'
service = Service(webdriver_path, log_path=logpath)
try:
    driver = webdriver.Chrome(service=service, options=options)
    print("WebDriver initialized successfully.")
except Exception:
    import traceback, os
    traceback.print_exc()
    if os.path.exists(logpath):
        print('\n=== chromedriver log ===')
        with open(logpath) as f:
            print(open(logpath).read()[-2000:])
    raise

# Navigate to the website
try:
    driver.get(website)
    print(f"Successfully navigated to {website}")
except Exception:
    print(f"Failed to navigate to {website}")
    traceback.print_exc()
# add scrolling to the bottom of the page to load all content
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)  # Wait for the page to load after scrolling
# Close the browser
driver.quit()