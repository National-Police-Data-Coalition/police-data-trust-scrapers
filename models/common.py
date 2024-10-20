from typing import Optional

from pydantic import BaseModel, Field


class PaginatedResponse(BaseModel):
    page: Optional[int] = Field(None, description="The current page number.")
    per_page: Optional[int] = Field(None, description="The number of items per page.")
    total: Optional[int] = Field(None, description="The total number of items.")
