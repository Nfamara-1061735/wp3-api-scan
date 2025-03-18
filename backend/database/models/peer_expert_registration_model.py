from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend import db


class PeerExpertRegistration(db.Model):
    __tablename__ = 'peer_expert_registrations'

    peer_expert_registration_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    """ID of the registration"""

    registration_status_id: Mapped[int] = mapped_column(ForeignKey('registration_statuses.registration_status_id'))
    """Foreign key to the status."""

    peer_expert_id: Mapped[int] = mapped_column(ForeignKey('peer_experts.peer_expert_id'))
    """Foreign key to the target peer expert."""

    research_id: Mapped[int] = mapped_column(ForeignKey('researches.research_id'))
    """Foreign key to the target research."""

    registration_status: Mapped["RegistrationStatus"] = relationship("RegistrationStatus",
                                                                     backref="peer_expert_registrations")
    """Relationship to the RegistrationStatus model"""
