from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.models.research_model import Research
from backend import db

class LimitationsModel(db.Model):
    """limitations Table"""
    __tablename__ = 'limitations'

    limitation_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    """ID for limitation(s)"""

    limitation: Mapped[str]
    """limitation"""

    limitation_category: Mapped[str]
    """limitation category"""

    researches: Mapped[list["Research"]] = relationship(secondary="research_limitations", back_populates="limitations")