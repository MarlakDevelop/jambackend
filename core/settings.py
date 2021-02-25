import os
from datetime import timedelta


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret key lol')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_USERNAME_KEY = 'username'
    JWT_AUTH_HEADER_PREFIX = 'Token'
    CORS_HEADERS = 'Content-Type'
    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:4200',
        'http://localhost:4200',
    ]
    JWT_HEADER_TYPE = 'Token'
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'jam.db'
    DB_PATH = os.path.join(PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(10 ** 6)
