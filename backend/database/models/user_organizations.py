from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from backend import db

class UserOrganization(db.Model):
    """Lists who works for what company."""
    __tablename__ = 'user_organizations'

    user_organizations_id: Mapped[int] = mapped_column(primary_key=True)
    """Unique identifier for the user organization link."""

    has_reward: Mapped[bool]
    """Indicates if this user has admin privileges within this company."""

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    """Foreign key to the employee user."""

    organization_id: Mapped[int] = mapped_column(ForeignKey('user_organizations.organization_id'))
    """Foreign key to the employing company."""