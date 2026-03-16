from flask import jsonify, request

from ..services import record_service
from ..utils.errors import unauthorized, bad_request


def register_record_routes(app, current_user):
    @app.post("/api/teacher-records")
    def create_teacher_record():
        user = current_user()
        if not user:
            return unauthorized()

        data = request.json or {}
        record, err = record_service.create_teacher_record(user.id, data)
        if err:
            return bad_request(err)
        return jsonify({"message": "老师数据已记录"})

    @app.post("/api/parent-records")
    def create_parent_record():
        user = current_user()
        if not user:
            return unauthorized()

        data = request.json or {}
        record, err = record_service.create_parent_record(user.id, data)
        if err:
            return bad_request(err)
        return jsonify({"message": "家长记录已保存"})

    @app.get("/api/checkin")
    def get_checkin():
        user = current_user()
        if not user:
            return unauthorized()

        today_record, streak, month_records = record_service.get_checkin_stats(user.id)
        return jsonify(
            {
                "todayDone": bool(today_record and today_record.done),
                "streak": streak,
                "monthCount": month_records,
            }
        )

    @app.post("/api/checkin")
    def do_checkin():
        user = current_user()
        if not user:
            return unauthorized()

        record_service.do_checkin(user.id)
        return jsonify({"message": "已打卡"})


__all__ = ["register_record_routes"]

