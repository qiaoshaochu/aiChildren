from datetime import datetime

from models import db


class Analysis(db.Model):
    __tablename__ = "analyses"

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey("children.id"), nullable=False)
    analysis_date = db.Column(db.Date, nullable=False)
    trend = db.Column(db.String(50))
    insights = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


__all__ = ["Analysis"]

