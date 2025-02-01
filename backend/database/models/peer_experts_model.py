import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from backend import db


class PeerExperts(db.Model):
    __tablename__ = "peer_experts"

    peer_experts_id: Mapped[int] = mapped_column(primary_key=True)
    postal_code: Mapped[str]
    gender: Mapped[str]
    birth_date: Mapped[datetime.datetime]
    tools_used: Mapped[Optional[str]]
    short_bio: Mapped[str]
    special_notes:Mapped[Optional[str]]
    accepted_terms:Mapped[bool]
    is_supervisor: Mapped[bool]
    supervisor_or_gardian_name: Mapped[Optional[str]]
    availability_notes: Mapped[str]
    # foreignkeys
    contact_preference_id: Mapped[int] = mapped_column(ForeignKey('contact_preferences.contact_preference_id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))

    





