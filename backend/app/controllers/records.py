from flask import Blueprint, jsonify, request

from ..services import record_service
from ..utils.errors import bad_request

bp = Blueprint("records", __name__, url_prefix="/api/records")


@bp.route("", methods=["POST"])
def create_record():
    # MVP 阶段暂不鉴权
    data = request.get_json() or {}
    record, err = record_service.create_record(data)
    if err:
        return bad_request(err)
    return jsonify(_serialize_record(record)), 201


@bp.route("", methods=["GET"])
def list_records():
    # MVP 阶段暂不鉴权
    child_id_raw = request.args.get("child_id")
    records, err = record_service.list_records_by_child(child_id_raw)
    if err:
        return bad_request(err)
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
