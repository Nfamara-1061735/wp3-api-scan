from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import ForeignKey

from backend import db

class ResearchLimitations(db.Model):
    """Research limitations Table"""
    __tablename__ = 'research_limitations'

    research_limitation_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    """ID for research limitation"""

    research_id: Mapped[int] = mapped_column(ForeignKey("researches.research_id"), nullable=False)
    """ID for research"""

    limitation_id: Mapped[int] = mapped_column(ForeignKey("limitations.beperking_id"), nullable=False)
    """ID for limitation"""