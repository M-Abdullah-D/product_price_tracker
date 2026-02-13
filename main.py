from config import options
from driver import initialize_driver
from scraper import extract_book_urls
from parser import extract_book_data
from storage import save_to_csv
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




def main():
    driver= initialize_driver(options)
    try:
        URLs=extract_book_urls(driver)
        for url in URLs[:5]:
            extract_book_data(driver, url)
        save_to_csv(str(input("Enter the filename to save the data (without extension): ")+".csv"))
    finally:
        driver.quit()
        logging.info("WebDriver closed successfully.")


if __name__ == "__main__":
    main()