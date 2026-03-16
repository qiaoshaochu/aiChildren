from datetime import datetime, timedelta

from ..models import db
from ..models.record import TeacherRecord, ParentRecord, Checkin, Record


def create_teacher_record(user_id, payload):
    date_str = payload.get("date")
    topic = payload.get("topic", "")
    status = payload.get("status", "正常")
    learned = payload.get("learned", "")
    note = payload.get("note", "")

    try:
        date = (
            datetime.fromisoformat(date_str).date()
            if date_str
            else datetime.utcnow().date()
        )
    except ValueError:
        return None, "日期格式不正确"

    record = TeacherRecord(
        user_id=user_id,
        date=date,
        topic=topic,
        status=status,
        learned=learned,
        note=note,
    )
    db.session.add(record)
    db.session.commit()
    return record, None


def create_parent_record(user_id, payload):
    date_str = payload.get("date")
    task_done = bool(payload.get("task_done"))
    reading = bool(payload.get("reading"))
    interaction = bool(payload.get("interaction"))
    note = payload.get("note", "")

    try:
        date = (
            datetime.fromisoformat(date_str).date()
            if date_str
            else datetime.utcnow().date()
        )
    except ValueError:
        return None, "日期格式不正确"

    record = ParentRecord(
        user_id=user_id,
        date=date,
        task_done=task_done,
        reading=reading,
        interaction=interaction,
        note=note,
    )
    db.session.add(record)
    db.session.commit()
    return record, None


def get_checkin_stats(user_id):
    today = datetime.utcnow().date()
    today_record = Checkin.query.filter_by(user_id=user_id, date=today).first()

    streak = 0
    d = today
    while True:
        r = Checkin.query.filter_by(user_id=user_id, date=d).first()
        if r and r.done:
            streak += 1
            d -= timedelta(days=1)
        else:
            break

    month_start = today.replace(day=1)
    month_records = Checkin.query.filter(
        Checkin.user_id == user_id,
        Checkin.date >= month_start,
        Checkin.date <= today,
        Checkin.done.is_(True),
    ).count()

    return today_record, streak, month_records


def do_checkin(user_id):
    today = datetime.utcnow().date()
    record = Checkin.query.filter_by(user_id=user_id, date=today).first()
    if not record:
        record = Checkin(user_id=user_id, date=today, done=True)
        db.session.add(record)
    else:
        record.done = True
    db.session.commit()
    return record


def create_record(payload):
    """MVP Record 模型：创建一条记录."""
    child_id = payload.get("child_id")
    record_date_str = payload.get("record_date")
    category = payload.get("category", "").strip()
    value = payload.get("value", "").strip()
    notes = payload.get("notes", "")

    if not child_id:
        return None, "child_id 必填"
    if not category:
        return None, "category 必填"
    if not value:
        return None, "value 必填"

    try:
        record_date = (
            datetime.fromisoformat(record_date_str).date()
            if record_date_str
            else datetime.utcnow().date()
        )
    except (ValueError, TypeError):
        return None, "record_date 格式不正确"

    record = Record(
        child_id=int(child_id),
        record_date=record_date,
        category=category[:20],
        value=value[:50],
        notes=notes or None,
    )
    db.session.add(record)
    db.session.commit()
    return record, None


def list_records_by_child(child_id):
    """MVP Record 模型：按 child_id 列表."""
    return Record.query.filter_by(child_id=int(child_id)).order_by(
        Record.record_date.desc(), Record.created_at.desc()
    ).all()


__all__ = [
    "create_teacher_record",
    "create_parent_record",
    "get_checkin_stats",
    "do_checkin",
    "create_record",
    "list_records_by_child",
]

