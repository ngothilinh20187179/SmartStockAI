from __future__ import annotations

from pydantic import BaseModel


class Pagination(BaseModel):
    total: int
    limit: int
    offset: int

