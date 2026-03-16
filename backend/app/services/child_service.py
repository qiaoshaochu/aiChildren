from datetime import datetime

from ..models import db
from ..models.child import Child


def create_child(payload):
    name = payload.get("name", "").strip()
    if not name:
        return None, "姓名为必填"
    birth_date = payload.get("birth_date")
    gender = payload.get("gender", "")
    avatar_url = payload.get("avatar_url", "")

    try:
        bd = datetime.fromisoformat(birth_date).date() if birth_date else None
    except (ValueError, TypeError):
        bd = None

    child = Child(
        name=name,
        birth_date=bd,
        gender=gender[:10] if gender else None,
        avatar_url=avatar_url[:255] if avatar_url else None,
    )
    db.session.add(child)
    db.session.commit()
    return child, None


def get_child_by_id(child_id):
    return Child.query.get(child_id)


__all__ = ["create_child", "get_child_by_id"]
