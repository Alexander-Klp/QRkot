from sqlalchemy import Column, String, Text

from app.models.base import CommonColumns


class CharityProject(CommonColumns):
    name = Column(String(100), nullable=False)
    description = Column(Text)

    def __repr__(self):
        return (
            f'name = {self.name} '
            f'create_date = {self.create_date} '
            f'close_date = {self.close_date} '
        )
