from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import CommonColumns


class Donation(CommonColumns):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'user.id = {self.user_id}'
        )
