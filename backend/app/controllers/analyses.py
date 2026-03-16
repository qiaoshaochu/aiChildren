from flask import Blueprint, jsonify, request, g

from ..services import analysis_service
from ..utils.errors import unauthorized, bad_request

bp = Blueprint("analyses", __name__, url_prefix="/api/analyses")


def _require_user():
    user = getattr(g, "current_user", None)
    if not user:
        return None
    return user


@bp.route("", methods=["POST"])
def create_analysis():
    if _require_user() is None:
        return unauthorized()
    data = request.get_json() or {}
    analysis, err = analysis_service.create_analysis(data)
    if err:
        return bad_request(err)
    return jsonify(_serialize_analysis(analysis)), 201


@bp.route("", methods=["GET"])
def list_analyses():
    if _require_user() is None:
        return unauthorized()
    child_id = request.args.get("child_id")
    if not child_id:
        return bad_request("缺少 child_id")
    try:
        child_id = int(child_id)
    except ValueError:
        return bad_request("child_id 必须为数字")
    analyses = analysis_service.list_analyses_by_child(child_id)
    return jsonify([_serialize_analysis(a) for a in analyses])


def _serialize_analysis(a):
    return {
        "id": a.id,
        "child_id": a.child_id,
        "analysis_date": a.analysis_date.isoformat() if a.analysis_date else None,
        "trend": a.trend,
        "insights": a.insights,
        "recommendations": a.recommendations,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }
