from sqlalchemy.orm import Mapped, mapped_column

from backend import db


class OrganizationType(db.Model):
    __tablename__ = 'organization_types'

    organization_type_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    """ID from organization type"""

    type: Mapped[str]
    """defines current type of the organization"""