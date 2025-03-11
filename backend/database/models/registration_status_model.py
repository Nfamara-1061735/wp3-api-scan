from sqlalchemy.orm import Mapped, mapped_column

from backend import db


class RegistrationStatus(db.Model):
    __tablename__ = 'registration_statuses'

    registration_status_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    """ID of the status"""

    status: Mapped[str]
    """defines a status name"""
