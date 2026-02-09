from paths import webdriver_path, browser_path, profile_path


# Adding the path to the webdriver and the browser
webdriver_path=webdriver_path
browser_path=browser_path
profile_path=profile_path

# Adding the domain and the category pages to be scraped
domain="https://www.amazon.com"
book_shelf="Best-Sellers-Books-Business-Development-Entrepreneurship/zgbs/books/2741"
page_num=["1","2"]
for page in page_num:
    website=f"{domain}/{book_shelf}/?_encoding=UTF8&pg={page}"