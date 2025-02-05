from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from backend import db

class LimitationsModel(db.Model):
    """limitations Table"""
    __tablename__ = 'limitations'

    limitation_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    """ID for limitation(s)"""

    limitation: Mapped[str]
    """limitation"""