import os

from urllib.parse import quote


class Config:

    SECRET_KEY = '3dcd49b05133792807b7844555a3a921'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:%s@localhost/flask_db" % quote('Simform@123')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """ Mail Configuration """
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'fantasticsingh99@gmail.com'
    MAIL_PASSWORD = 'iurwwdxkltpgiytk'

    """SIJAX (Simple Ajax) Configurations"""
    SIJAX_STATIC_PATH = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
    SIJAX_JSON_URI = '/static/js/sijax/json2.js'

    SQLALCHEMY_ECHO = True
