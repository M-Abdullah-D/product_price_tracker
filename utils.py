from config import XPATHS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import logging



def change_currency(driver):
    try:
        sleep(3)
        Selcting_currency(
            driver, "currency_list", "Clicked on the currency list."
        )
        Selcting_currency(
            driver, "currency_element", "Selected the desired currency."
        )
    except Exception as e:
        logging.error(f"Failed to change currency: {e}")

def Selcting_currency(driver, arg1, arg2):
        # Click on the currency list to open the dropdown
    currency_list = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, XPATHS[arg1]))
    )
    currency_list.click()
    logging.info(arg2)


def scroll_the_page(driver):
    try:
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)  # Wait for the page to load
            if len(driver.find_elements(By.XPATH, XPATHS["end_of_page"])) > 0:
                logging.info("Reached the end of the page.")
                break
    except Exception as e:
        logging.error(f"Failed to scroll to the end of the page: {e}")