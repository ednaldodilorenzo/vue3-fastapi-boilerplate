import math
from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field, computed_field

M = TypeVar("M")


class PaginatedResponse(BaseModel, Generic[M]):
    count: int = Field(description="Number of items returned in the response")
    items: List[M] = Field(description="List of items returned in the response following given criteria")
    page: int = Field(description="Selected page")
    page_size: int

    @computed_field
    @property
    def total_pages(self) -> int:
        return math.ceil(self.count / self.page_size)
