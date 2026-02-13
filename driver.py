from config import temp_profile_dir
import logging
import traceback
import os
from selenium import webdriver
from paths import webdriver_path
from selenium.webdriver.chrome.service import Service


# service configuration and error handling
logpath = 'chromedriver_test.log'
service = Service(webdriver_path, log_path=logpath)

def initialize_driver(options):
    try:
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("WebDriver initialized successfully.")
        return driver
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