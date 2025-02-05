from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from backend import db

class PeerExpertsResearchTypes(db.Model):
    __tablename__ = "peer_experts_research_types"

    expert_research_types_id: Mapped[int] = mapped_column(primary_key=True)

    peer_expert_id: Mapped[int] = mapped_column(ForeignKey('peer_experts.peer_expert_id'))
    research_type_id: Mapped[int] = mapped_column(ForeignKey('research_types.research_type_id'))