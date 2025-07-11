# ardurHealthcare/app/__init__.py
from flask import Flask, session, flash, render_template
from flask_login import LoginManager
from .config import Config
import os

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    print("🔧 Creating Flask app...")

    # --- START OF REQUIRED CHANGE ---
    # Get the absolute path to the directory containing this __init__.py file (ardurHealthcare/app)
    app_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one level to the project root (ardurHealthcare)
    project_root = os.path.join(app_dir, '..')

    app = Flask(
        __name__,
        template_folder=os.path.join(app_dir, 'templates'), # This is the default, but explicit is good
        static_folder=os.path.join(project_root, 'static') # TELL FLASK WHERE YOUR STATIC FOLDER IS
    )
    # --- END OF REQUIRED CHANGE ---

    print("🔑 Loading configuration...")
    app.config.from_object(config_class)

    required_configs = ['SECRET_KEY', 'JSON_STORAGE_PATH']
    print("📦 Validating required configs...")
    for config_item in required_configs:
        if config_item not in app.config:
            raise ValueError(f"❌ Missing required config: {config_item}")
        print(f"✅ Config {config_item}: {app.config[config_item]}")

    try:
        print(f"📂 Ensuring JSON storage path exists: {app.config['JSON_STORAGE_PATH']}")
        os.makedirs(app.config['JSON_STORAGE_PATH'], exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to create storage directory: {str(e)}")

    print("🔐 Initializing Flask-Login...")
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        print(f"🔎 Loading user: {username}")
        try:
            from .auth.models import User
            return User.get(username)
        except Exception as e:
            app.logger.error(f"❌ Error loading user: {str(e)}")
            return None

    # Register blueprints
    try:
        print("📌 Registering blueprints...")

        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        print("✅ Registered auth blueprint.")

        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        print("✅ Registered main blueprint.")

        from .contact import contact as contact_blueprint
        app.register_blueprint(contact_blueprint)
        print("✅ Registered contact blueprint.")

        from .services import services as services_blueprint
        app.register_blueprint(services_blueprint)
        print("✅ Registered services blueprint.")

        from .resources import resources as resources_blueprint
        app.register_blueprint(resources_blueprint)
        print("✅ Registered resources blueprint.")

        from .specialities import specialities as specialities_blueprint
        app.register_blueprint(specialities_blueprint)
        print("✅ Registered specialities blueprint.")

        from .ourreach import ourreach as ourreach_blueprint
        app.register_blueprint(ourreach_blueprint, url_prefix='/state')
        print("✅ Registered ourreach blueprint.")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to register blueprints: {str(e)}")

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    @app.errorhandler(404)
    def not_found_error(error):
        print("🚫 404 Error occurred.")
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        print("🔥 500 Error occurred.")
        return render_template('errors/500.html'), 500

    print("🗺️ Listing all registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"🔗 {rule} -> {rule.endpoint}")

    print("✅ Flask app created successfully.")
    return app
