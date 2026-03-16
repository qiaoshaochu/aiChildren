from flask import Blueprint, jsonify, request, g

from ..services import record_service
from ..utils.errors import unauthorized, bad_request

bp = Blueprint("records", __name__, url_prefix="/api/records")


def _require_user():
    user = getattr(g, "current_user", None)
    if not user:
        return None
    return user


@bp.route("", methods=["POST"])
def create_record():
    if _require_user() is None:
        return unauthorized()
    data = request.get_json() or {}
    record, err = record_service.create_record(data)
    if err:
        return bad_request(err)
    return jsonify(_serialize_record(record)), 201


@bp.route("", methods=["GET"])
def list_records():
    if _require_user() is None:
        return unauthorized()
    child_id = request.args.get("child_id")
    if not child_id:
        return bad_request("缺少 child_id")
    try:
        child_id = int(child_id)
    except ValueError:
        return bad_request("child_id 必须为数字")
    records = record_service.list_records_by_child(child_id)
    return jsonify([_serialize_record(r) for r in records])


def _serialize_record(r):
    return {
        "id": r.id,
        "child_id": r.child_id,
        "record_date": r.record_date.isoformat() if r.record_date else None,
        "category": r.category,
        "value": r.value,
        "notes": r.notes,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }
