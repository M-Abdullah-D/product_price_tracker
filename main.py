import argparse
import logging
from config import options
from driver import driver_context
from scraper import extract_book_urls
from parser import extract_book_data
from storage import save_to_csv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def build_parser():
    p = argparse.ArgumentParser(description="Product price tracker scraper")
    p.add_argument("-o", "--output", default="Scraped_books.csv", help="Output CSV filename")
    p.add_argument("-n", "--max-books", type=int, default=0, help="Maximum number of books to scrape (0 = all)")
    p.add_argument("--headless", action="store_true", help="Run browser in headless mode (overrides config)")
    p.add_argument("--start-page", type=int, default=1, help="Start page for pagination")
    p.add_argument("--page-limit", type=int, default=0, help="Limit number of pages to visit (0 = all)")
    p.add_argument("--log-level", default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR)")
    return p


def apply_cli_to_options(opt, args):
    # opt is the ChromeOptions object from config; adjust it based on flags
    if args.headless:
        try:
            # remove any existing headless flags then add the requested one
            # (some versions use '--headless=new' or '--headless', adapt if needed)
            opt.add_argument("--headless=new")
        except Exception:
            opt.add_argument("--headless")
    # You can add other option toggles here (proxy, user-agent, etc.)
    return opt


def main():
    parser = build_parser()
    args = parser.parse_args()
   
        # Prompt for output filename if not provided via CLI
    if  args.output:
        args.output = input("Enter output CSV filename: ").strip()
    if not args.output:
            args.output = "Scraped_books.csv"
    
    # Ensure .csv extension
    if not args.output.endswith('.csv'):
        args.output += '.csv'
   
   # Only prompt if not provided via CLI
    if args.max_books == 0:
        args.max_books = int(input("Specify the number of books to scrape (0 for all): ") or 0)
    
    # Validate
    if args.max_books < 0:
        logger.error("max_books must be non-negative")
        return
    

    # set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper(), logging.INFO))

    # mutate options only at runtime per flags (safe because we import the object)
    apply_cli_to_options(options, args)

    books = []
    with driver_context(options) as driver:
        urls = extract_book_urls(driver)
        if args.max_books and args.max_books > 0:
            urls = urls[: args.max_books]

        for i, url in enumerate(urls, start=1):
            logger.info("Processing %s/%s: %s", i, len(urls), url)
            book = extract_book_data(driver, url)
            books.append(book)
            if args.max_books and i >= args.max_books:
                break

    save_to_csv(args.output, books)
    logger.info("Saved %s books to %s", len(books), args.output)


if __name__ == "__main__":
    main()