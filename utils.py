from config import XPATHS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import logging



def change_currency(driver): 
    try:
        sleep(2)
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
    currency_list = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, XPATHS[arg1]))
    )
    currency_list.click()
    logging.info(arg2)


def scroll_the_page(driver):
    sleep(3)  # Wait for the page to stabilize before scrolling
    try:
        while True:
            element = driver.find_element(By.XPATH, XPATHS["end_of_page"])
            driver.execute_script("arguments[0].scrollIntoView();", element)
            sleep(2)  # Wait for the page to load
            if len(driver.find_elements(By.XPATH, XPATHS["end_of_page"])) > 0:
                logging.info("Reached the end of the page.")
                break
    except Exception as e:
        logging.error(f"Failed to scroll to the end of the page: {e}")












    # try:
    #     sleep(3)  # Wait for the page to stabilize before clicking
    #     currency_list_element = WebDriverWait(driver, 3).until(
    #         EC.element_to_be_clickable((By.XPATH, '//*[@id="icp-nav-flyout"]/button'))
    #     )
    #     currency_list_element.click()
    #     currency_element = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-flyout-icp"]/div[2]/ul[2]/li[2]/a'))
    #     )
    #     currency_element.click()
    #     logging.info("Currency changed successfully.")
    #     sleep(2)  # Wait for the currency change to complete
    # except Exception:
    #     logging.info("Failed to change currency.")
    #     traceback.print_exc()