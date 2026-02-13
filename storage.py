import pandas as pd
import logging
from models import Title_list, Author_list, Reviews_Rate_list, Reviews_Number_list, Kindle_price_list, Audiobook_price_list, Hardcover_price_list, Paperback_price_list



def create_dataframe():
    """Create a DataFrame from a list of Book objects."""
    data = {
        "Title": Title_list,
        "Author": Author_list,
        "Reviews_Rate": Reviews_Rate_list,
        "Reviews_Number": Reviews_Number_list,
        "Kindle_Price": Kindle_price_list,
        "Audiobook_Price": Audiobook_price_list,
        "Hardcover_Price": Hardcover_price_list,
        "Paperback_Price": Paperback_price_list
    }
    df = pd.DataFrame(data)
    logging.info("DataFrame created successfully.")
    return df

def save_to_csv(filename):
    """Save the DataFrame to a CSV file."""
    df = create_dataframe()
    df.to_csv(filename, index=False)
    logging.info(f"Data saved to {filename} successfully.")
