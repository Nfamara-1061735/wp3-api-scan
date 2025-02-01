from backend import db


class ResearchStatus(db.Model):
    __tablename__ = 'research_statuses'

    research_status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(45), nullable=False)
