from backend import db


class ResearchStatus(db.Model):
    __tablename__ = 'research_statuses'

    research_status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(45), nullable=False)

    # def __repr__(self):
    #     return f"<ResearchStatus(id={self.research_status_id}, status='{self.status}')>"

    @staticmethod
    def get_status_by_id(status_id):
        return db.session.query(ResearchStatus).filter_by(research_status_id=status_id).first()