from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend import db


class PeerExpertsLimitations(db.Model):
    __tablename__ = "peer_experts_limitations"

    peer_expert_limitation_id: Mapped[int] = mapped_column(primary_key=True)

    limitation_id: Mapped[int] = mapped_column(ForeignKey('limitations.limitation_id'))
    peer_expert_id: Mapped[int] = mapped_column(ForeignKey('peer_experts.peer_expert_id'))

    # Explicit typing for clarity
    limitation: Mapped["LimitationsModel"] = relationship(
        "LimitationsModel",
        backref="peer_experts_limitations"
    )