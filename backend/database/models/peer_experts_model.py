import datetime
from typing import Optional
from sqlalchemy import ForeignKey
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from backend import db

class PeerExperts(db.Model):
    __tablename__ = "peer_experts"

    peer_expert_id: Mapped[int] = mapped_column(primary_key=True)
    postal_code: Mapped[str]
    gender: Mapped[str]
    birth_date: Mapped[datetime.datetime] = mapped_column(sa.Date) #only shows Date without time
    tools_used: Mapped[Optional[str]]
    short_bio: Mapped[str]
    special_notes:Mapped[Optional[str]] 
    accepted_terms:Mapped[bool] = mapped_column(default=False)
    has_supervisor: Mapped[bool] = mapped_column(default=False)
    supervisor_or_guardian_name: Mapped[Optional[str]]
    availability_notes: Mapped[str]

    contact_preference_id: Mapped[int] = mapped_column(ForeignKey('contact_preferences.contact_preference_id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))

    user: Mapped["Users"] = relationship(back_populates="peer_expert_info")
