import math
from typing import Generic, TypeVar

T = TypeVar("T")


class PagedResponse(Generic[T]):
    def __init__(self, items: list[T], total: int, page: int, size: int):
        self.items = items
        self.total = total
        self.page = page
        self.size = size
        self.pages = math.ceil(total / size) if size > 0 else 0

    def to_dict(self) -> dict:
        return {
            "items": self.items,
            "total": self.total,
            "page": self.page,
            "size": self.size,
            "pages": self.pages,
        }
