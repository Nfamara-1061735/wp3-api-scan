import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from backend import db

class Research(db.Model):
    """Researches Table"""
    __tablename__ = 'researches'

    research_id: Mapped[int] = mapped_column(primary_key=True)
    """Unique identifier for the research."""

    title: Mapped[str]
    """The title of the research study."""

    is_available: Mapped[bool]
    """Indicates if the research is available."""

    description: Mapped[Optional[str]]
    """Description of the research."""

    start_date: Mapped[datetime.datetime]
    """The start date and time of the research."""

    end_date: Mapped[datetime.datetime]
    """The end date and time of the research."""

    location: Mapped[str]
    """Location where the research takes place."""

    has_reward: Mapped[bool]
    """Indicates if there is a reward."""

    reward: Mapped[Optional[str]]
    """Describes what the reward of this research is."""

    target_min_age: Mapped[Optional[int]]
    """Minimum age for peer experts."""

    target_max_age: Mapped[Optional[int]]
    """Maximum age for peer experts."""

    # Define foreign key relationships
    status_id: Mapped[int] = mapped_column(ForeignKey('research_statuses.research_status_id'))
    """Foreign key to the research status."""

    research_type_id: Mapped[int] = mapped_column(ForeignKey('research_types.research_type_id'))
    """Foreign key to the research type."""