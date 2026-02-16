import math
from typing import Generic, List, TypeVar

from sqlalchemy.orm import Query

T = TypeVar("T")


class Pagination(Generic[T]):
    def __init__(self, items: List[T], total: int, page: int, limit: int):
        self.items = items
        self.page = page
        self.limit = limit
        self.total = total
        self.total_pages = math.ceil(self.total / self.limit)
        self.has_previous_page = self.page > 1
        self.has_next_page = self.page < self.total_pages

    def meta_dict(self):
        return {
            "total": self.total,
            "total_pages": self.total_pages,
            "current_page": self.page,
            "limit": self.limit,
            "has_previous_page": self.has_previous_page,
            "has_next_page": self.has_next_page,
        }


def paginate(query: Query, page: int, limit: int) -> Pagination:
    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()
    return Pagination(items, total, page, limit)