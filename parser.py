import logging
from selenium.webdriver.common.by import By
import traceback
from typing import Tuple
from models import Book
from config import XPATHS
from selenium.common.exceptions import NoSuchElementException, TimeoutException

logger = logging.getLogger(__name__)


def _get_text(driver, xpath: str) -> str:
    """Return element text for xpath or empty string if missing."""
    try:
        el = driver.find_element(By.XPATH, xpath)
        return el.text.strip()
    except Exception:
        logger.debug("Element not found for xpath %s", xpath, exc_info=True)
        return ""


def extract_format_price(driver, label_xpath_key: str, price_xpath_key: str) -> str:
    """Return price text for a specific format or empty string."""
    try:
        label = _get_text(driver, XPATHS.get(label_xpath_key))
        if not label:
            return ""
        price = _get_text(driver, XPATHS.get(price_xpath_key))
        return price or ""
    except Exception:
        logger.debug("Failed to extract format price for %s", price_xpath_key, exc_info=True)
        return ""





def extract_title(driver) -> str:
    return _get_text(driver, XPATHS.get("title_element"))


def extract_author(driver) -> str:
    return _get_text(driver, XPATHS.get("Author_element"))

def extract_reviews(driver) -> Tuple[str, str]:
    rate = _get_text(driver, XPATHS.get("Reviews_Rate_element"))
    number = _get_text(driver, XPATHS.get("Reviews_Number_element"))
    return rate, number

def extract_prices(driver) -> Tuple[str, str, str, str]:
    kindle = extract_format_price(driver, "Kindle", "Kindle_price_element")
    audiobook = extract_format_price(driver, "Audiobook", "Audiobook_price_element")
    hardcover = extract_format_price(driver, "Hardcover", "Hardcover_price_element")
    paperback = extract_format_price(driver, "Paperback", "Paperback_price_element")
    return kindle, audiobook, hardcover, paperback


def extract_book_data(driver, url: str) -> Book:
    """Navigate to `url` and return a populated Book object (never mutate globals)."""
    book = Book(url=url)
    try:
        driver.get(url)
        logger.info("Navigated to %s", url)

        book.title = extract_title(driver)
        book.author = extract_author(driver)
        book.reviews_rate, book.reviews_number = extract_reviews(driver)
        (book.kindle_price,
         book.audiobook_price,
         book.hardcover_price,
         book.paperback_price) = extract_prices(driver)

    except Exception:
        logger.exception("Failed to extract book data for %s", url)
    return book