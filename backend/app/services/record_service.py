from datetime import datetime, timedelta

from ..models import db
from ..models.record import TeacherRecord, ParentRecord, Checkin, Record
from ..utils.validation import parse_date, parse_child_id


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
    """MVP Record 模型：创建一条记录，校验在 service 层."""
    child_id_raw = payload.get("child_id")
    cid, err = parse_child_id(child_id_raw)
    if err:
        return None, err
    record_date_raw = payload.get("record_date")
    record_date, err = parse_date(record_date_raw, default_today=True)
    if err:
        return None, "record_date " + err
    category = (payload.get("category") or "").strip()
    value = (payload.get("value") or "").strip()
    notes = (payload.get("notes") or "").strip() or None

    if not category:
        return None, "category 必填"
    if not value:
        return None, "value 必填"

    record = Record(
        child_id=cid,
        record_date=record_date,
        category=category[:20],
        value=value[:50],
        notes=notes,
    )
    db.session.add(record)
    db.session.commit()
    return record, None


def list_records_by_child(child_id_raw):
    """MVP Record 模型：按 child_id 列表，校验在 service 层."""
    cid, err = parse_child_id(child_id_raw)
    if err:
        return None, err
    records = Record.query.filter_by(child_id=cid).order_by(
        Record.record_date.desc(), Record.created_at.desc()
    ).all()
    return records, None


__all__ = [
    "create_teacher_record",
    "create_parent_record",
    "get_checkin_stats",
    "do_checkin",
    "create_record",
    "list_records_by_child",
]

