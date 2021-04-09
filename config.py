from dotenv import load_dotenv
from tempfile import mkdtemp
import os

load_dotenv()

class Config:


    # app general
    SECRET_KEY = os.getenv('SECRET_KEY')
    TEMPLATES_AUTO_RELOAD = True
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # app session
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    # database
    password = os.getenv('mysql_key')
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://MarcMartinho:{}@MarcMartinho.mysql.pythonanywhere-services.com/users".format(password)
    #SQLALCHEMY_DATABASE_URI = "mysql://MarcMartinho:{DB_PW}@MarcMartinho.mysql.pythonanywhere-services.com/users.db".format(DB_PW)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
