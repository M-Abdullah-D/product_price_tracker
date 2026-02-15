from config import temp_profile_dir
import logging
import traceback
import os
from selenium import webdriver
from paths import webdriver_path
from selenium.webdriver.chrome.service import Service
from contextlib import contextmanager


# service configuration and error handling
logpath = 'chromedriver_test.log'
service = Service(webdriver_path, log_path=logpath)

@contextmanager
def driver_context(options):
    """
    Context manager that yields a WebDriver instance and ensures it is properly closed, with error handling for initialization and cleanup.
    """
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("Webdriver initialized successfully")
        yield driver
    except Exception:
        logging.exception("Failed to initialize WebDriver.")
        if os.path.exists(logpath):
            logging.info("Printing tail of chromedriver log for diagnosis:")
            with open(logpath, 'r') as f:
                logging.info(f.read()[-2000:])
        if temp_profile_dir is not None:
            try:
                temp_profile_dir.cleanup()
            except Exception:
                logging.exception("Failed to clean up temporary Chrome profile directory.")
        raise
    finally:
        if driver is not None:
            try:
                driver.quit()
                logging.info("WebDriver closed successfully.")
            except Exception:
                logging.exception("Failed to close WebDriver properly.")
        if temp_profile_dir is not None:
            try:
                temp_profile_dir.cleanup()
                logging.info("Temporary Chrome profile directory cleaned up successfully.")
            except Exception:
                logging.exception("Failed to clean up temporary Chrome profile directory.")







