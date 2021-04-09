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
    username = 'MarcMartinho'
    server = 'MarcMartinho.mysql.pythonanywhere-services.com'
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{server}/users".format(username, password, server)
    #SQLALCHEMY_DATABASE_URI = "mysql://MarcMartinho:{DB_PW}@MarcMartinho.mysql.pythonanywhere-services.com/users.db".format(DB_PW)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
