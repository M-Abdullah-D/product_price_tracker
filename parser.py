import logging
from selenium.webdriver.common.by import By
import traceback
from models import Title_list, Author_list, Reviews_Rate_list, Reviews_Number_list, Kindle_price_list, Paperback_price_list, Hardcover_price_list, Audiobook_price_list


def extract_element_text(driver, xpath, target_list, success_message, failure_message):
    """Extract text from an element by XPath and append to a list."""
    try:
        element = driver.find_element(By.XPATH, xpath)
        text = element.text
        target_list.append(text)
        logging.info(success_message)
    except Exception:
        logging.info(failure_message)
        target_list.append("X")


def extract_format_price(driver, format_name, format_index, price_list):
    """Extract price for a specific book format."""
    try:
        format_element = driver.find_element(By.XPATH, f'//*[@id="a-autoid-{format_index}-announce"]/span[1]/span')
        if format_element.text == format_name:
            price_element = driver.find_element(By.XPATH, f'//*[@id="a-autoid-{format_index}-announce"]/span[2]/span')
            price = price_element.text
            price_list.append(price)
            logging.info(f"Successfully extracted the {format_name} price.")
        else:
            logging.info(f"{format_name} version not available.")
            price_list.append("X")
    except Exception:
        logging.info(f"{format_name} version not available.")
        price_list.append("X")





def extract_title(driver):
    extract_element_text(
        driver,
        '//*[@id="productTitle"]',
        Title_list,
        "Successfully extracted the book title.",
        "Failed to extract the book title."
    )


def extract_author(driver):
    extract_element_text(
        driver,
        '//*[@id="bylineInfo"]/span[1]/a',
        Author_list,
        "Successfully extracted the author name.",
        "Failed to extract the author name."
    )

def extract_reviews(driver):
    extract_element_text(
        driver,
        '//*[@id="acrPopover"]/span/a/span',
        Reviews_Rate_list,
        "Successfully extracted the reviews information.",
        "Failed to extract the reviews information."
    )
    extract_element_text(
        driver,
        '//*[@id="acrCustomerReviewText"]',
        Reviews_Number_list,
        "Successfully extracted the reviews information.",
        "Failed to extract the reviews information."
    )

def extract_prices(driver):
    extract_format_price(driver, "Kindle", 0, Kindle_price_list)
    extract_format_price(driver, "Audiobook", 1, Audiobook_price_list)
    extract_format_price(driver, "Hardcover", 2, Hardcover_price_list)
    extract_format_price(driver, "Paperback", 3, Paperback_price_list)


def extract_book_data(driver, url):
    """Navigate to the book URL and extract all relevant data."""
    try:
        driver.get(url)
        logging.info(f"Navigated to {url} successfully.")
        extract_title(driver)
        extract_author(driver)
        extract_reviews(driver)
        extract_prices(driver)
    except Exception:
        logging.info(f"Failed to navigate to {url} or extract data.")
        traceback.print_exc()