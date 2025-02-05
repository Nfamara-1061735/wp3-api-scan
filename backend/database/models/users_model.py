from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from backend import db

class Users(db.Model):
    """Users Table"""
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    """ID for identifying the user"""

    first_name: Mapped[str]
    """First name of the user"""

    last_name: Mapped[str]
    """Last name of the user"""

    email: Mapped[str]
    """Email of the user"""

    phone_number: Mapped[str]
    """phone number of the user"""

    password: Mapped[str]
    """password of the user"""

    salt: Mapped[str]
    """hashed password of the user"""