from sqlalchemy.orm import Mapped, mapped_column
from backend import db

class ApiKeys(db.Model):
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    api_key: Mapped[str] = mapped_column(unique=True, nullable=False)
