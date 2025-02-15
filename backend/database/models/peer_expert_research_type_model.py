from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import ForeignKey

from backend import db

class PeerExpertResearchTypeModel(db.Model):
    """peer_expert_research_type Table"""
    __tablename__ = 'peer_expert_research_type'

    expert_research_type_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True, unsigned=True)
    """ID for identification of expert research type"""

    peer_expert_id: Mapped[int] = mapped_column(ForeignKey('peer_experts.peer_expert_id'), nullable=False)
    """ID for peer expert"""

    research_type_id: Mapped[int] = mapped_column(ForeignKey('research_types.research_type_id'), nullable=False)
    """ID for research type"""