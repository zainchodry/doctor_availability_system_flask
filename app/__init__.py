from flask import Flask
from app.extenshions import *
from app.models import *
from flask_login import current_user
from config import Config
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.abspath('templates'))
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.routes.admin import admin_bp
    from app.routes.doctor import doctor_bp
    from app.routes.auth import auth_bp
    from app.routes.patient import patient_bp

    app.register_blueprint(patient_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)
    
    login_manager.login_view = "auth.login"
    login_manager.session_protection = "strong"

    with app.app_context():
        db.create_all()

    return app