from ..models import db
from ..models.child import Child
from ..utils.validation import parse_date


def create_child(payload):
    name = (payload.get("name") or "").strip()
    if not name:
        return None, "姓名为必填"
    birth_date_raw = payload.get("birth_date")
    bd, err = parse_date(birth_date_raw, default_today=False)
    if err:
        return None, err
    gender = (payload.get("gender") or "")[:10]
    avatar_url = (payload.get("avatar_url") or "")[:255]

    child = Child(
        name=name,
        birth_date=bd,
        gender=gender if gender else None,
        avatar_url=avatar_url if avatar_url else None,
    )
    db.session.add(child)
    db.session.commit()
    return child, None


def get_child_by_id(child_id):
    return Child.query.get(child_id)


__all__ = ["create_child", "get_child_by_id"]
