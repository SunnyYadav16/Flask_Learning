import os


class Config:
    SECRET_KEY = '3dcd49b05133792807b7844555a3a921'
    SQLALCHEMY_DATABASE_URI = "sqlite:///learning.db"

    """ Mail Configuration """
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'fantasticsingh99@gmail.com'
    MAIL_PASSWORD = 'iurwwdxkltpgiytk'

    """SIJAX (Simple Ajax) Configurations"""
    SIJAX_STATIC_PATH = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
    SIJAX_JSON_URI = '/static/js/sijax/json2.js'
