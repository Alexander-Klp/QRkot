from typing import Optional

from pydantic import BaseModel, Extra, Field, validator
from typing_extensions import Annotated

from app.schemas.base import CommontFieldsBase


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: Annotated[int, Field(strict=True, gt=0)]


class CharityProjectCreate(CharityProjectBase):

    class Config:
        extra = Extra.forbid

    @validator('name', 'description', 'full_amount')
    def field_cannot_empty_or_none(cls, value, field):
        if not value:
            raise ValueError(f'Поле: {field.name} не может быть пустым!')
        return value


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    full_amount: Optional[Annotated[int, Field(
        strict=True, gt=0
    )]] = Field(None)

    @validator('name', 'description', 'full_amount')
    def field_cannot_empty_or_none(cls, value, field):
        if field.name == 'full_amount' and (value is None or value <= 0):
            raise ValueError(f'Поле "{field.name}" должно быть больше 0.')
        if not value:
            raise ValueError(f'Поле "{field.name}" не может быть пустым!')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CommontFieldsBase, CharityProjectBase):
    pass
