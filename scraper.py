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


def extract_book_urls(driver):
    books_urls = []
    last_page = get_last_page(driver)
    current_page = 1

    while current_page <= last_page:
        try:
            logger.info(f"Processing page {current_page} of {last_page}")
            navigate_to_website(driver, current_page)
            if current_page == 1:
                change_currency(driver)
            scroll_the_page(driver)
            sleep(2)  # Wait for the book list to load after currency change

            books = driver.find_elements(By.XPATH, XPATHS["books"])
            logger.info("Found %s books on page %s", len(books), current_page)
            for item in books:
                try:
                    url = item.find_element(By.XPATH, XPATHS["URL"]).get_attribute('href')
                    books_urls.append(url)
                except Exception:
                    logger.exception("Failed to extract book URL from an item")
            logger.info("Extracted URLs (total): %s", len(books_urls))

            current_page += 1
            try:
                next_page = driver.find_element(By.XPATH, XPATHS["next_page"])
                next_page.click()
            except Exception:
                logger.info("No next-page element found; finishing pagination")
                break
        except Exception:
            logger.exception("Error while processing page %s", current_page)
            break

    return books_urls