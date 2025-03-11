from sqlalchemy.orm import Mapped, mapped_column

from backend import db


class PeerExpertStatus(db.Model):
    __tablename__ = 'peer_expert_statuses'

    peer_expert_status_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    """ID of the status"""

    status: Mapped[str]
    """defines a status name"""
