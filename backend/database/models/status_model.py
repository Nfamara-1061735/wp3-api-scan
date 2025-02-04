from sqlalchemy.orm import Mapped, mapped_column

from backend import db


class ResearchStatus(db.Model):
    __tablename__ = 'research_statuses'

    research_status_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True, unsigned=True)
    """ID from research status"""

    status: Mapped[str]
    """defines current status of the research"""