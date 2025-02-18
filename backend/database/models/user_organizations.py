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

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    """Foreign key to the employee user."""

    is_admin: Mapped[bool]
    """Indicates if this user has admin privileges within this company."""

    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.organization_id'))
    """Foreign key to the employing company."""