from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from backend import db

class ResearchTypesModel(db.Model):
    """research types Table"""
    __tablename__ = 'research_types'

    research_type_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    """ID for research type"""

    type: Mapped[str]
    """type of research type"""