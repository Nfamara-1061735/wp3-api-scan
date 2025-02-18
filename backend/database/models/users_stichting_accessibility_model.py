from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from backend import db

class UsersStichtingAccessibility(db.Model):
    """Users of stichting accessibility Table"""
    __tablename__ = 'users_stichting_accessibility'

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True, nullable=False, unique=True)
    """ID from users"""

    admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    """defines if user is admin or not"""