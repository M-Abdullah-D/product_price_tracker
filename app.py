from paths import webdriver_path, browser_path, profile_path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback, os


# Adding the domain and the category pages to be scraped
domain="https://www.amazon.com"
book_shelf="Best-Sellers-Books-Business-Development-Entrepreneurship/zgbs/books/2741"
page=2
website=f"{domain}/{book_shelf}/?_encoding=UTF8&pg={page}&language=en_US&currency=USD"

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
# options.add_argument("--headless=new")      # Uncomment this after we make sure the code is working, this will run the browser in headless mode

# service configuration and error handling
logpath = 'chromedriver_test.log'
service = Service(webdriver_path, log_path=logpath)
try:
    driver = webdriver.Chrome(service=service, options=options)
    print("WebDriver initialized successfully.")
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
            print("Failed to clean up temporary Chrome profile directory:")
            traceback.print_exc()
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
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@id, "p13n-asin-index-49")]'))
    )
    print("Page loaded successfully after scrolling.")
except Exception:
    print("Failed to load the page after scrolling.")
    traceback.print_exc()
# table = driver.find_element("xpath", "//div[@id='zg-ordered-list']")









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