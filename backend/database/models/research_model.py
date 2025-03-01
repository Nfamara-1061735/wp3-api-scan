import datetime
from typing import Optional
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
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

    start_date: Mapped[datetime.datetime] = mapped_column(sa.Date)
    """The start date and time of the research."""

    end_date: Mapped[datetime.datetime] = mapped_column(sa.Date)
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
    """Foreign key to the current research status."""

    research_type_id: Mapped[int] = mapped_column(ForeignKey('research_types.research_type_id'))
    """Foreign key to the type of research."""

    def __init__(self, title, is_available, description, start_date, end_date, location, has_reward, reward, target_min_age, target_max_age, status_id, research_type_id):
        self.title = title
        self.is_available = is_available
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.has_reward = has_reward
        self.reward = reward
        self.target_min_age = target_min_age
        self.target_max_age = target_max_age
        self.status_id = status_id
        self.research_type_id = research_type_id

    def __repr__(self):
        return f"Onderzoek(title = {self.title}, is_availeble = {self.is_available}, description = {self.description}, start_date = {self.start_date}, end_date = {self.end_date}, location = {self.location}, has_reward = {self.has_reward}, reward = {self.reward}, target_min_age = {self.target_min_age}, target_max_age = {self.target_max_age})"