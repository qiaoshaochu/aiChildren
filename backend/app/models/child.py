from datetime import datetime

from models import db


class Child(db.Model):
    __tablename__ = "children"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    avatar_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    records = db.relationship("Record", backref="child", lazy=True)
    analyses = db.relationship("Analysis", backref="child", lazy=True)


__all__ = ["Child"]

