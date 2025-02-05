from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import ForeignKey

from backend import db

class Organizations(db.Model):
    """Organizations Table"""
    __tablename__ = 'organizations'

    organization_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    """ID for identifying the organization"""

    name: Mapped[str]
    """name of organization"""

    website: Mapped[str]
    """website of organization"""

    description: Mapped[str]
    """description with """

    contact_person: Mapped[str]
    """contact person of organization"""

    email: Mapped[str]
    """email of organization"""

    phone_number: Mapped[str]
    """phone number of organization"""

    additional_information: Mapped[str]
    """additional information about organization"""

    organization_types: Mapped[int] = mapped_column(ForeignKey("organization_types.organization_type_id"),nullable=False)
    """?"""
