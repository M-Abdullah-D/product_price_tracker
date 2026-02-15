from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Book:
    title: str = ""
    author: str = ""
    reviews_rate: float = 0.0
    reviews_number: int = 0
    kindle_price: float = 0.0
    audiobook_price: float = 0.0
    hardcover_price: float = 0.0
    paperback_price: float = 0.0
    url: str = ""


Books = List[Book]

    