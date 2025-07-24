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

    # Flask-Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@ardurhealthcare.com'

    # Email recipients
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'abhi@ardurtechnology.com'
    ANALYTICS_EMAIL = os.environ.get('ANALYTICS_EMAIL') or 'analytics@ardurhealthcare.com'

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
