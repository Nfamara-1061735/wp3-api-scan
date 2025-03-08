from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from backend import db

class ContactPreferences(db.Model):
    __tablename__ = "contact_preferences"

    contact_preference_id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] 



