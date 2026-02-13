from config import website
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import traceback
from models import books_URLs
from time import sleep
from selenium.webdriver.common.by import By
from utils import change_currency, scroll_the_page





def navigate_to_website(driver, page_number=None):
    driver.get(website)
    if page_number:
        logging.info(f"Successfully navigated to page {page_number}")
    else:
        logging.info(f"Successfully navigated to {website}")


def get_last_page(driver):
    """Extract the last page number from pagination."""
    navigate_to_website(driver)
    pagination = driver.find_element(By.XPATH, '//*[contains(@class,"a-pagination")]')
    pages = pagination.find_elements(By.XPATH, "./li")
    return int(pages[-2].text)


def extract_book_urls(driver):
    try:
        last_page = get_last_page(driver)
        current_page = 1

        while current_page <= last_page:
            try:
                navigate_to_website(driver, current_page)
                if current_page == 1:
                    change_currency(driver)
                scroll_the_page(driver)
                sleep(2)  # Wait for the book list to load after currency change
                books = driver.find_elements(By.XPATH, '//*[contains(@class,"zg-no-numbers")]')
                logging.info(f"Found {len(books)} books on the page.")
                for book in books: 
                    try:
                        URL = book.find_element(By.XPATH, './/span/div/div/div/div[2]/span/div/div/div/a').get_attribute('href')
                        books_URLs.append(URL)
                    except Exception:
                        logging.info("Failed to extract book information.")
                        traceback.print_exc()
                logging.info(f"Extracted URLs: {len(books_URLs)}")
            # Going to the next page
                current_page+=1
                try:
                    next_page=driver.find_element(By.XPATH, '//*[@id="CardInstanceTJXUd2yD4hIsSwroLLmNtw"]/div[2]/nav/ul/li[4]')
                    next_page.click()
                except Exception:
                    logging.info("Last page reached")
            except Exception:
                logging.info(f"Failed to navigate to {website}")
                traceback.print_exc()
    except Exception:
        logging.info(f"Failed to navigate to {website}")
        traceback.print_exc()
    return books_URLs