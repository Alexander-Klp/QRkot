from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommontFieldsBase(BaseModel):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime] = Field(default=None)

    class Config:
        orm_mode = True
