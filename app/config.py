import os

class Config:
    # Base directory of the application
    BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # JSON storage configuration
    JSON_STORAGE_PATH = os.path.join(BASEDIR, 'data')
    USERS_FILE = os.path.join(JSON_STORAGE_PATH, 'users.json')
    CONTACTS_FILE = os.path.join(JSON_STORAGE_PATH, 'contacts.json')
    
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