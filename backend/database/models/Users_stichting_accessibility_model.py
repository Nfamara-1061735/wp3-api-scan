from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from backend import db

class UsersStichtingAccessibility(db.Model):
    """Users of stichting accessibility Table"""
    __tablename__ = 'users_stichting_accessibility'

    gebruikers_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True, unsigned=True)
    """ID from users"""

    admin: Mapped[bool] = mapped_column(nullable=False)
    """defines if user is admin or not"""

    gebruiker_werkt_voor_stichting_accessibilitycol: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    """defines if user works for stichting accessibility or not"""