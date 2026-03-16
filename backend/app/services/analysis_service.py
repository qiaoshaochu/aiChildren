from datetime import datetime

from ..models import db
from ..models.analysis import Analysis


def create_analysis(payload):
    child_id = payload.get("child_id")
    analysis_date_str = payload.get("analysis_date")
    trend = payload.get("trend", "")
    insights = payload.get("insights", "")
    recommendations = payload.get("recommendations", "")

    if not child_id:
        return None, "child_id 必填"

    try:
        analysis_date = (
            datetime.fromisoformat(analysis_date_str).date()
            if analysis_date_str
            else datetime.utcnow().date()
        )
    except (ValueError, TypeError):
        return None, "analysis_date 格式不正确"

    analysis = Analysis(
        child_id=int(child_id),
        analysis_date=analysis_date,
        trend=trend[:50] if trend else None,
        insights=insights or None,
        recommendations=recommendations or None,
    )
    db.session.add(analysis)
    db.session.commit()
    return analysis, None


def list_analyses_by_child(child_id):
    return Analysis.query.filter_by(child_id=int(child_id)).order_by(
        Analysis.analysis_date.desc(), Analysis.created_at.desc()
    ).all()


__all__ = ["create_analysis", "list_analyses_by_child"]
