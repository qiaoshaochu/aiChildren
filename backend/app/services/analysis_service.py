from ..models import db
from ..models.analysis import Analysis
from ..utils.validation import parse_date, parse_child_id


def create_analysis(payload):
    child_id_raw = payload.get("child_id")
    cid, err = parse_child_id(child_id_raw)
    if err:
        return None, err
    analysis_date_raw = payload.get("analysis_date")
    analysis_date, err = parse_date(analysis_date_raw, default_today=True)
    if err:
        return None, "analysis_date " + err

    trend = (payload.get("trend") or "")[:50] or None
    insights = (payload.get("insights") or "").strip() or None
    recommendations = (payload.get("recommendations") or "").strip() or None

    analysis = Analysis(
        child_id=cid,
        analysis_date=analysis_date,
        trend=trend,
        insights=insights,
        recommendations=recommendations,
    )
    db.session.add(analysis)
    db.session.commit()
    return analysis, None


def list_analyses_by_child(child_id_raw):
    cid, err = parse_child_id(child_id_raw)
    if err:
        return None, err
    analyses = Analysis.query.filter_by(child_id=cid).order_by(
        Analysis.analysis_date.desc(), Analysis.created_at.desc()
    ).all()
    return analyses, None


__all__ = ["create_analysis", "list_analyses_by_child"]
