from config import website, XPATHS
import logging
logger = logging.getLogger(__name__)
import traceback
from time import sleep
from selenium.webdriver.common.by import By
from utils import change_currency, scroll_the_page


def navigate_to_website(driver, page_number=None):
    base = website.split('?')[0]
    url = base if page_number is None else f"{base}?_encoding=UTF8&pg={page_number}&language=en_US&currency=USD"
    driver.get(url)
    if page_number:
        logger.info("Successfully navigated to page %s", page_number)
    else:
        logger.info("Successfully navigated to %s", website)


def get_last_page(driver):
    """Extract the last page number from pagination (safe fallback to 1)."""
    try:
        navigate_to_website(driver)
        pagination = driver.find_element(By.XPATH, XPATHS["pagination"])
        pages = pagination.find_elements(By.XPATH, XPATHS["pages"])
        return int(pages[-2].text) if len(pages) >= 2 else 1
    except Exception:
        logger.exception("Failed to determine last page; defaulting to 1")
        return 1


def extract_book_urls(driver,start_page:int,page_limit:int):
    books_urls = []
    last_page = get_last_page(driver)
    if page_limit == 0:
        end_page = last_page 
    else:
        min(start_page + page_limit -1,last_page)     # if the page limit is given the value of 0 it should go for all
 
    if start_page < 1:
        logger.error("The pages start with page 1")
        return[]
    if page_limit <0: 
        logger.error("The number of pages to navigate can not be negative")
        return[]
    if start_page > last_page:
        logger.error("The start page is out of the available page range")
        return[]

    for _ in range(start_page, end_page + 1):
        try:
            logger.info(f"Processing page {start_page} of {end_page}")
            navigate_to_website(driver, start_page)
            if start_page == 1:
                change_currency(driver)
            scroll_the_page(driver)
            sleep(2)  # Wait for the book list to load after currency change

            books = driver.find_elements(By.XPATH, XPATHS["books"])
            logger.info("Found %s books on page %s", len(books), start_page)
            for item in books:
                try:
                    url = item.find_element(By.XPATH, XPATHS["URL"]).get_attribute('href')
                    books_urls.append(url)
                except Exception:
                    logger.exception("Failed to extract book URL from an item")
            logger.info("Extracted URLs (total): %s", len(books_urls))

            start_page += 1
        except Exception:
            logger.exception("Error while processing page %s", start_page)
            break

    return books_urls