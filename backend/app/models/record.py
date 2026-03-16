from datetime import datetime

from ...models import db, TeacherRecord, ParentRecord, Checkin  # noqa: F401


class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey("children.id"), nullable=False)
    record_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    value = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


__all__ = ["TeacherRecord", "ParentRecord", "Checkin", "Record"]

