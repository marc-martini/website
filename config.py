from dotenv import load_dotenv
from tempfile import mkdtemp
import os

load_dotenv()

class Config:
    
    # app general
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TEMPLATES_AUTO_RELOAD = True
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
    # app session
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    
    # database
    SQLALCHEMY_DATABASE_URI = "sqlite:///stocks.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False