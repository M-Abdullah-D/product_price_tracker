import pandas as pd
import logging
from dataclasses import asdict
from typing import List
from models import Book

logger = logging.getLogger(__name__)


def create_dataframe(books: List[Book]) -> pd.DataFrame:
    """Create a DataFrame from a list of Book objects."""
    rows = [asdict(b) for b in books]
    df = pd.DataFrame(rows)
    logger.info("DataFrame created successfully. Rows=%s", len(df))
    return df


def save_to_csv(filename: str, books: List[Book]) -> None:
    """Save the provided books to a CSV file."""
    df = create_dataframe(books)
    df.to_csv(filename, index=False)
    logger.info("Data saved to %s successfully.", filename)
