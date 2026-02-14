from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Book:
    title: str = ""
    author: str = ""
    reviews_rate: str = ""
    reviews_number: str = ""
    kindle_price: str = ""
    audiobook_price: str = ""
    hardcover_price: str = ""
    paperback_price: str = ""
    url: str = ""


Books = List[Book]

    