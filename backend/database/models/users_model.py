from enum import unique
from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from backend import db

class Users(db.Model):
    """Users Table"""
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    """ID for identifying the user"""

    first_name: Mapped[str]
    """First name of the user"""

    last_name: Mapped[str]
    """Last name of the user"""

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    """Email of the user"""

    phone_number: Mapped[str]
    """phone number of the user"""

    password: Mapped[bytes]
    """password of the user"""

    salt: Mapped[bytes]
    """hashed password of the user"""

    peer_expert_info: Mapped["PeerExperts"] = relationship(back_populates="user")
    admin_info: Mapped["UsersStichtingAccessibility"] = relationship(back_populates="user")
    organizations: Mapped[List["UserOrganization"]] = relationship(back_populates="user")
