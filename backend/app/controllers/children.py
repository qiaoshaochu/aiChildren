from flask import Blueprint, jsonify, request, g

from ..services import child_service
from ..utils.errors import unauthorized, bad_request

bp = Blueprint("children", __name__, url_prefix="/api/children")


def _require_user():
    user = getattr(g, "current_user", None)
    if not user:
        return None
    return user


@bp.route("", methods=["POST"])
def create_child():
    if _require_user() is None:
        return unauthorized()
    data = request.get_json() or {}
    child, err = child_service.create_child(data)
    if err:
        return bad_request(err)
    return jsonify(_serialize_child(child)), 201


@bp.route("/<int:child_id>", methods=["GET"])
def get_child(child_id):
    if _require_user() is None:
        return unauthorized()
    child = child_service.get_child_by_id(child_id)
    if not child:
        return jsonify({"error": "孩子不存在"}), 404
    return jsonify(_serialize_child(child))


def _serialize_child(c):
    return {
        "id": c.id,
        "name": c.name,
        "birth_date": c.birth_date.isoformat() if c.birth_date else None,
        "gender": c.gender,
        "avatar_url": c.avatar_url,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "updated_at": c.updated_at.isoformat() if c.updated_at else None,
    }
