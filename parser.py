import logging
from selenium.webdriver.common.by import By
from typing import Tuple
from models import Book
from config import XPATHS
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


def _get_text(driver, xpath: str) -> str:
    """Return element text for xpath or empty string if missing."""
    try:
        el = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath)))
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
            return None
        price = float(_get_text(driver, XPATHS.get(price_xpath_key)).strip("$"))
        return price or None
    except Exception:
        logger.debug("Failed to extract format price for %s", price_xpath_key, exc_info=True)
        return ""





def extract_title(driver) -> str:
    return _get_text(driver, XPATHS.get("title_element"))


def extract_author(driver) -> str:
    return _get_text(driver, XPATHS.get("Author_element"))

def extract_reviews(driver) -> Tuple[float, int]:
    rate = _get_text(driver, XPATHS.get("Reviews_Rate_element"))
    number = _get_text(driver, XPATHS.get("Reviews_Number_element"))
    try:
        rate = float(rate.strip()) if rate else 0.0
        number = int(number.replace(',', '').replace('(', '').replace(')', '').replace('"', '').strip()) if number else 0
    except ValueError:
        logger.warning("Failed to convert review data to numbers.")
        rate = 0.0
        number = 0
    return rate, number

def extract_prices(driver) -> Tuple[float, float, float, float]:
    kindle = extract_format_price(driver, "Kindle", "Kindle_price_element")
    audiobook = extract_format_price(driver, "Audiobook", "Audiobook_price_element")
    hardcover = extract_format_price(driver, "Hardcover", "Hardcover_price_element")
    paperback = extract_format_price(driver, "Paperback", "Paperback_price_element")
    return kindle, audiobook, hardcover, paperback


def _navigate_to_url(driver, url: str) -> None:
    """Navigate to the specified URL and log the action."""
    driver.get(url)
    logger.info("Navigated to %s", url)


def extract_book_data(driver, url: str) -> Book:
    """Navigate to `url` and return a populated Book object (never mutate globals)."""
    book = Book(url=url)
    try:
        _navigate_to_url(driver, url)  # Wait for the page to load; consider replacing with explicit waits for better performance
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