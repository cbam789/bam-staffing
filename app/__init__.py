from flask import Flask
from flask_login import LoginManager
from .models import db, User


def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecret"  # Use environment variable in prod

    # ✅ SQLite config for now — swap with PostgreSQL later
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ Init DB
    db.init_app(app)

    # ✅ Init LoginManager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # ✅ Load user from DB for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from app.routes import main_bp
    from app.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # ✅ Mount Dash here
    from app.dash_app import create_dash_app

    create_dash_app(app)

    with app.app_context():
        db.create_all()

    return app
