from flask import Flask, request, session, g
from flask_cors import CORS
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from .config import init_config
from .models import db, init_db, User
from .controllers import register_routes
from .controllers.children import bp as children_bp
from .controllers.records import bp as records_bp
from .controllers.analyses import bp as analyses_bp


def create_app():
    app = Flask(__name__)
    init_config(app)

    CORS(app, supports_credentials=True)
    init_db(app)

    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"], salt="aiChildren-auth")

    def issue_token(user: User) -> str:
        return serializer.dumps({"uid": user.id, "role": user.role})

    def verify_token(token: str):
        try:
            data = serializer.loads(token, max_age=60 * 60 * 24 * 30)
            return data
        except (BadSignature, SignatureExpired):
            return None

    def current_user():
        from .models import User as UserModel  # late import to avoid cycles

        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth.removeprefix("Bearer ").strip()
            data = verify_token(token)
            if data and data.get("uid"):
                return UserModel.query.get(int(data["uid"]))

        uid = session.get("user_id")
        if not uid:
            return None
        return UserModel.query.get(uid)

    @app.before_request
    def inject_current_user():
        g.current_user = current_user()

    # 原有路由
    register_routes(app, current_user, issue_token)

    # REST API Blueprints
    app.register_blueprint(children_bp)
    app.register_blueprint(records_bp)
    app.register_blueprint(analyses_bp)

    return app


__all__ = ["create_app", "db"]

