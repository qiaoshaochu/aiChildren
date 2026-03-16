from datetime import datetime, timedelta

from flask import jsonify, request, session

from ..models import db, User, TeacherRecord, ParentRecord, BusybookItem
from .record import register_record_routes


def register_routes(app, current_user, issue_token):
    # -------- 认证 --------
    @app.post("/api/auth/register")
    def register():
        data = request.json or {}
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        role = data.get("role", "parent")

        if not username or not password:
            return jsonify({"error": "用户名和密码必填"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "用户名已存在"}), 400

        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "注册成功"})

    @app.post("/api/auth/login")
    def login():
        data = request.json or {}
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({"error": "用户名或密码错误"}), 401

        session["user_id"] = user.id
        session["role"] = user.role
        token = issue_token(user)
        return jsonify(
            {
                "message": "登录成功",
                "user": {"id": user.id, "username": user.username, "role": user.role},
                "token": token,
            }
        )

    @app.post("/api/auth/logout")
    def logout():
        session.clear()
        return jsonify({"message": "已登出"})

    # 注册记录相关路由（老师/家长记录 + 打卡）
    register_record_routes(app, current_user)

    # -------- 首页数据 --------
    @app.get("/api/home")
    def home():
        user = current_user()
        if not user:
            return jsonify({"error": "未登录"}), 401

        today = datetime.utcnow().date()

        base_tasks = [
            "今天和孩子说 3 次颜色英文",
            "找 2 个圆形物品",
            "读 1 本绘本",
        ]
        today_tasks = [{"id": i + 1, "title": t} for i, t in enumerate(base_tasks)]

        teacher_record = (
            TeacherRecord.query.filter(TeacherRecord.date == today)
            .order_by(TeacherRecord.created_at.desc())
            .first()
        )
        if teacher_record:
            today_class = {
                "topic": teacher_record.topic,
                "status": teacher_record.status,
                "learned": teacher_record.learned,
                "note": teacher_record.note,
            }
        else:
            today_class = None

        start_of_week = today - timedelta(days=today.weekday())
        week_parent_records = ParentRecord.query.filter(
            ParentRecord.date >= start_of_week, ParentRecord.date <= today
        ).all()

        total_days = len(week_parent_records)
        done_reading = sum(1 for r in week_parent_records if r.reading)
        done_interaction = sum(1 for r in week_parent_records if r.interaction)

        summary = "本周数据较少，继续保持记录哦。"
        if total_days >= 3:
            if done_interaction >= total_days * 0.6:
                summary = "本周家庭互动次数提升，孩子更愿意参与活动。"
            elif done_reading >= total_days * 0.6:
                summary = "本周亲子阅读较稳定，继续保持共读习惯。"
            else:
                summary = "本周任务完成度一般，可以尝试固定一个陪伴时间。"

        return jsonify(
            {
                "todayTasks": today_tasks,
                "todayClass": today_class,
                "weekSummary": summary,
            }
        )

    # -------- 数据看板 --------
    @app.get("/api/dashboard")
    def dashboard():
        user = current_user()
        if not user:
            return jsonify({"error": "未登录"}), 401

        today = datetime.utcnow().date()
        seven_days_ago = today - timedelta(days=6)

        teacher_records = (
            TeacherRecord.query.filter(
                TeacherRecord.date >= seven_days_ago, TeacherRecord.date <= today
            )
            .order_by(TeacherRecord.date.asc())
            .all()
        )
        parent_records = (
            ParentRecord.query.filter(
                ParentRecord.date >= seven_days_ago, ParentRecord.date <= today
            )
            .order_by(ParentRecord.date.asc())
            .all()
        )

        def serialize_teacher(r: TeacherRecord):
            return {
                "date": r.date.isoformat(),
                "topic": r.topic,
                "status": r.status,
                "learned": r.learned,
                "note": r.note,
            }

        def serialize_parent(r: ParentRecord):
            return {
                "date": r.date.isoformat(),
                "task_done": r.task_done,
                "reading": r.reading,
                "interaction": r.interaction,
                "note": r.note,
            }

        total_teacher = len(teacher_records)
        total_parent = len(parent_records)
        reading_days = sum(1 for r in parent_records if r.reading)
        interaction_days = sum(1 for r in parent_records if r.interaction)

        learned_topics = [r.topic for r in teacher_records if r.topic]
        learned_str = "、".join(learned_topics) if learned_topics else "基础互动主题"

        summary_ai = (
            f"本周共记录老师上课 {total_teacher} 次、家庭记录 {total_parent} 天。"
            f"主要学习了：{learned_str}。"
        )
        summary_ai += f" 家庭阅读完成 {reading_days} 天，亲子互动完成 {interaction_days} 天。"
        summary_ai += " 整体参与度良好，建议下周继续保持稳定的家庭陪伴节奏。"

        def level_text(ratio: float):
            if ratio >= 0.7:
                return "优秀"
            if ratio >= 0.4:
                return "略高于平均"
            return "正常区间"

        if total_parent:
            reading_ratio = reading_days / total_parent
            interaction_ratio = interaction_days / total_parent
            task_ratio = sum(1 for r in parent_records if r.task_done) / total_parent
        else:
            reading_ratio = interaction_ratio = task_ratio = 0.0

        peer = {
            "expression": level_text(interaction_ratio),
            "reading": level_text(reading_ratio),
            "task": level_text(task_ratio),
        }

        return jsonify(
            {
                "teacherData": [serialize_teacher(r) for r in teacher_records],
                "parentData": [serialize_parent(r) for r in parent_records],
                "aiSummary": summary_ai,
                "peerReference": peer,
            }
        )

    # -------- Busybook --------
    @app.get("/api/busybook")
    def list_busybook():
        user = current_user()
        if not user:
            return jsonify({"error": "未登录"}), 401

        items = BusybookItem.query.order_by(BusybookItem.created_at.desc()).all()
        return jsonify(
            [
                {
                    "id": i.id,
                    "image_url": i.image_url,
                    "title": i.title,
                    "child_age": i.child_age,
                    "likes": i.likes,
                    "created_at": i.created_at.isoformat(),
                }
                for i in items
            ]
        )

    @app.post("/api/busybook")
    def create_busybook():
        user = current_user()
        if not user:
            return jsonify({"error": "未登录"}), 401

        data = request.json or {}
        image_url = data.get("image_url", "")
        title = data.get("title", "")
        child_age = data.get("child_age", "")

        if not image_url:
            return jsonify({"error": "图片地址必填（可先用占位符）"}), 400

        item = BusybookItem(
            user_id=user.id,
            image_url=image_url,
            title=title,
            child_age=child_age,
        )
        db.session.add(item)
        db.session.commit()

        return jsonify({"message": "作品已上传", "id": item.id})

    @app.post("/api/busybook/<int:item_id>/like")
    def like_busybook(item_id: int):
        user = current_user()
        if not user:
            return jsonify({"error": "未登录"}), 401

        item = BusybookItem.query.get_or_404(item_id)
        item.likes += 1
        db.session.commit()
        return jsonify({"message": "已点赞", "likes": item.likes})

