import os
import sqlite3
from datetime import datetime
from pathlib import Path

import click
try:
    from flask import Flask, jsonify, request
except ImportError:
    print("Error: Flask not installed. Install it with: pip install flask")
    raise

try:
    from flask_cors import CORS
except ImportError:
    print("Warning: flask_cors not installed. Install it with: pip install flask-cors")
    CORS = lambda application: application

from flask_migrate import Migrate
from flask.cli import with_appcontext
from sqlalchemy import inspect
from werkzeug.security import check_password_hash, generate_password_hash

try:
    from .admin_routes import admin_bp
    from .career_routes import career_bp
    from .database import LEGACY_DB_PATH, get_database_uri, get_frontend_dir, load_json_data
    from .feedback_routes import feedback_bp
    from .job_routes import job_bp
    from .models import Admin, Career, Feedback, Job, LoginLog, User, db
    from .student_routes import student_bp
except ImportError:
    from admin_routes import admin_bp
    from career_routes import career_bp
    from database import LEGACY_DB_PATH, get_database_uri, get_frontend_dir, load_json_data
    from feedback_routes import feedback_bp
    from job_routes import job_bp
    from models import Admin, Career, Feedback, Job, LoginLog, User, db
    from student_routes import student_bp


migrate = Migrate()


def _get_json_payload():
    return request.get_json(silent=True) or {}


def _seed_default_admin():
    admin_username = os.getenv("SCA_ADMIN_USERNAME", "admin")
    admin_password = os.getenv("SCA_ADMIN_PASSWORD", "admin123")

    if Admin.query.filter_by(username=admin_username).first():
        return

    db.session.add(
        Admin(
            username=admin_username,
            password=generate_password_hash(admin_password),
            token=None,
        )
    )
    db.session.commit()


def _seed_default_careers():
    try:
        careers = load_json_data("careers.json")
    except (FileNotFoundError, OSError, ValueError):
        return

    existing_keys = set()
    has_changes = False

    for existing_career in Career.query.all():
        branch_key = (existing_career.branch or "").strip().lower()
        role_key = (existing_career.role or "").strip().lower()

        if role_key == "embedded systems engineer":
            db.session.delete(existing_career)
            has_changes = True
            continue

        existing_keys.add((branch_key, role_key))

    for item in careers:
        branch = (item.get("branch") or "").strip()
        role = (item.get("career") or "").strip()
        if not branch or not role:
            continue

        key = (branch.lower(), role.lower())
        if key in existing_keys:
            continue

        db.session.add(
            Career(
                branch=branch,
                role=role,
                required_skills=",".join(item.get("skills", [])),
                description=item.get("description", ""),
            )
        )
        existing_keys.add(key)
        has_changes = True

    if has_changes:
        db.session.commit()


def _record_login_activity(username, action, *, timestamp=None):
    if not username or action not in {"login", "logout"}:
        return

    db.session.add(
        LoginLog(
            username=username,
            action=action,
            timestamp=timestamp or datetime.utcnow(),
        )
    )


def _legacy_table_exists(cursor, table_name):
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    )
    return cursor.fetchone() is not None


def _migrate_legacy_feedback(cursor):
    if Feedback.query.count() > 0 or not _legacy_table_exists(cursor, "feedback"):
        return False

    cursor.execute("SELECT user_name, email, comments FROM feedback ORDER BY id ASC")
    rows = cursor.fetchall()

    for name, email, message in rows:
        db.session.add(Feedback(name=name or "", email=email or "", message=message or ""))

    return bool(rows)


def _migrate_legacy_jobs(cursor):
    if Job.query.count() > 0 or not _legacy_table_exists(cursor, "job_listings"):
        return False

    cursor.execute("SELECT title, company, description, skills FROM job_listings ORDER BY id ASC")
    rows = cursor.fetchall()

    for title, company, description, skills in rows:
        db.session.add(
            Job(
                company=company or "Unknown Company",
                role=title or "Untitled Role",
                location="",
                eligibility=description or skills or "",
                salary="",
            )
        )

    return bool(rows)


def _migrate_legacy_sqlite_data():
    legacy_path = Path(LEGACY_DB_PATH)
    if not legacy_path.exists():
        return

    connection = None
    try:
        connection = sqlite3.connect(legacy_path)
        cursor = connection.cursor()
        migrated_feedback = _migrate_legacy_feedback(cursor)
        migrated_jobs = _migrate_legacy_jobs(cursor)

        if migrated_feedback or migrated_jobs:
            db.session.commit()
    except sqlite3.Error:
        db.session.rollback()
    finally:
        if connection is not None:
            connection.close()


def _database_schema_ready():
    inspector = inspect(db.engine)
    existing_tables = set(inspector.get_table_names())
    required_tables = {
        Admin.__table__.name,
        Career.__table__.name,
        Feedback.__table__.name,
        Job.__table__.name,
        LoginLog.__table__.name,
        User.__table__.name,
    }
    return required_tables.issubset(existing_tables)


def initialize_app_data():
    if not _database_schema_ready():
        return False

    _seed_default_admin()
    _seed_default_careers()
    _migrate_legacy_sqlite_data()
    return True


def register_cli_commands(application):
    @application.cli.command("seed")
    @with_appcontext
    def seed():
        initialized = initialize_app_data()
        if initialized:
            click.echo("Application data initialized.")
            return

        click.echo(
            "Database schema is not ready yet. Run 'flask --app backend.app db upgrade' first."
        )


def create_app():
    frontend_dir = get_frontend_dir()
    application = Flask(__name__, static_folder=frontend_dir, static_url_path="")
    CORS(application)

    application.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    application.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

    db.init_app(application)
    migrate.init_app(application, db, directory=str(Path(__file__).resolve().parent / "migrations"))

    application.register_blueprint(admin_bp, url_prefix="/admin")
    application.register_blueprint(student_bp, url_prefix="/student")
    application.register_blueprint(feedback_bp, url_prefix="/api")
    application.register_blueprint(job_bp, url_prefix="/api")
    application.register_blueprint(career_bp, url_prefix="/api")

    register_cli_commands(application)

    @application.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    @application.route("/")
    def home():
        index_path = Path(application.static_folder or "") / "index.html"
        if not index_path.exists():
            return (
                jsonify(
                    {
                        "status": "ok",
                        "message": "Smart Career Advisor backend is running.",
                        "health": "/health",
                        "frontend": (
                            "Frontend files were not found in this deployment. "
                            "Deploy 'smart-career-advisor/smart-c-advisor' to Vercel "
                            "or set SCA_FRONTEND_DIR to a valid static directory."
                        ),
                    }
                ),
                200,
            )

        return application.send_static_file("index.html")

    return application


app = create_app()


@app.route("/login", methods=["POST"])
def login():
    data = _get_json_payload()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_time = datetime.utcnow()
        user.last_login = login_time
        _record_login_activity(user.username, "login", timestamp=login_time)
        db.session.commit()
        return jsonify({"message": "Login successful", "user": username}), 200

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/logout", methods=["POST"])
def logout():
    data = _get_json_payload()
    username = (data.get("username") or "").strip()

    if not username:
        return jsonify({"message": "Username required"}), 400

    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"message": "User not found"}), 404

    _record_login_activity(user.username, "logout")
    db.session.commit()

    return jsonify({"message": "Logout successful"}), 200


@app.route("/register", methods=["POST"])
def register():
    data = _get_json_payload()
    username = data.get("username")
    password = data.get("password")
    email = (data.get("email") or "").strip()

    if not username or not password or not email:
        return jsonify({"message": "Username, password, and email are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    db.session.add(User(username=username, password=generate_password_hash(password), email=email))
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201


if __name__ == "__main__":
    with app.app_context():
        initialize_app_data()
    app.run(debug=True)
