"""基础校验：日期格式等。"""
from datetime import datetime


def parse_date(value, default_today=False):
    """
    解析 ISO 日期 YYYY-MM-DD。
    - value: 字符串或 None。
    - default_today: 若 value 为空是否返回今天。
    返回 (date, None) 或 (None, "error_message")。
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        if default_today:
            return datetime.utcnow().date(), None
        return None, None
    if not isinstance(value, str):
        return None, "日期格式不正确，请使用 YYYY-MM-DD"
    value = value.strip()
    if len(value) != 10:
        return None, "日期格式不正确，请使用 YYYY-MM-DD"
    try:
        dt = datetime.fromisoformat(value)
        return dt.date(), None
    except (ValueError, TypeError):
        return None, "日期格式不正确，请使用 YYYY-MM-DD"


def parse_child_id(child_id_raw):
    """
    解析查询参数 child_id。
    返回 (int_child_id, None) 或 (None, "error_message")。
    """
    if child_id_raw is None or (isinstance(child_id_raw, str) and not child_id_raw.strip()):
        return None, "缺少 child_id"
    try:
        return int(child_id_raw), None
    except (ValueError, TypeError):
        return None, "child_id 必须为数字"


__all__ = ["parse_date", "parse_child_id"]
