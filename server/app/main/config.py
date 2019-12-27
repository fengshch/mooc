import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
# postgres_local_base = os.environ['DATABASE_URL']
postgres_local_base = "postgresql://bill:123456@172.16.12.216/"
database_dev = "mooc_dev"
database_test = "mooc_test"
database_prod = "mooc"


class Config:
    JWT_SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=43200)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(seconds=43200)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ERROR_MESSAGE_KEY = 'message'
    UPLOAD_FOLDER = '/var/media'
    MAX_CONTENT_LENGTH = 300 * 1024 * 1024
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'mooc_main.db')
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_dev
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'mooc_test.db')
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_test
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://mooc:mooc@postgres/mooc')


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
