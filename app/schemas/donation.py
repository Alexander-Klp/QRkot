from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field
from typing_extensions import Annotated

from app.schemas.base import CommontFieldsBase


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: Annotated[int, Field(strict=True, gt=0)]


class DonationCreate(DonationBase):

    class Config:
        extra = Extra.forbid


class DonationGetMy(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(CommontFieldsBase, DonationBase):
    user_id: int
