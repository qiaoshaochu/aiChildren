from flask import Blueprint, jsonify, request

from ..services import analysis_service
from ..utils.errors import bad_request

bp = Blueprint("analyses", __name__, url_prefix="/api/analyses")


@bp.route("", methods=["POST"])
def create_analysis():
    # MVP 阶段暂不鉴权
    data = request.get_json() or {}
    analysis, err = analysis_service.create_analysis(data)
    if err:
        return bad_request(err)
    return jsonify(_serialize_analysis(analysis)), 201


@bp.route("", methods=["GET"])
def list_analyses():
    # MVP 阶段暂不鉴权
    child_id_raw = request.args.get("child_id")
    analyses, err = analysis_service.list_analyses_by_child(child_id_raw)
    if err:
        return bad_request(err)
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
