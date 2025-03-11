from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from backend import db

class ApiKeys(db.Model):
    __tablename__ = "api_keys"

    api_key: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]