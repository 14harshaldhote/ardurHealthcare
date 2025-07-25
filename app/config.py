import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Base directory of the application
    BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'

    # JSON storage configuration
    JSON_STORAGE_PATH = os.path.join(BASEDIR, 'data')
    USERS_FILE = os.path.join(JSON_STORAGE_PATH, 'users.json')
    CONTACTS_FILE = os.path.join(JSON_STORAGE_PATH, 'contacts.json')

    # Flask-Mail configuration with performance optimizations
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # For local testing - no-reply email disabled, using admin email as sender
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'dhoteharshal16@gmail.com'

    # 🚀 PERFORMANCE OPTIMIZATION: Email timeouts to prevent hanging
    MAIL_TIMEOUT = int(os.environ.get('MAIL_TIMEOUT', '10'))  # 10 second timeout
    MAIL_CONNECTION_TIMEOUT = int(os.environ.get('MAIL_CONNECTION_TIMEOUT', '5'))  # 5 second connection timeout
    MAIL_MAX_RETRIES = int(os.environ.get('MAIL_MAX_RETRIES', '2'))  # Retry failed emails 2 times

    # Email recipients - only active emails for local testing
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'dhoteharshal16@gmail.com'
    ANALYTICS_EMAIL = os.environ.get('ANALYTICS_EMAIL') or 'dhoteh020@gmail.com'

    # Local testing mode - disable non-active emails
    ENABLE_ANALYTICS_EMAIL = os.environ.get('ENABLE_ANALYTICS_EMAIL', 'true').lower() in ['true', 'on', '1']

    # Application configuration
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
