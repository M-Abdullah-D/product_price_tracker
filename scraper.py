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


def extract_book_urls(driver,start_page,page_limit):
    books_urls = []
    last_page = get_last_page(driver)
    if page_limit == 0:
        page_limit = last_page       # if the page limit is given the value of 0 it should go for all

    while start_page <= page_limit:
        try:
            logger.info(f"Processing page {start_page} of {last_page}")
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