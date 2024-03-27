import os

from dotenv import load_dotenv

load_dotenv()


class DBConfig:
    HOST = os.getenv("DB_HOST", "localhost")
    PWD = os.getenv("DB_PASSWORD", "sqlite")
    USER = os.getenv("DB_USER", "sqlite")
    NAME = os.getenv("DB_NAME", "finance_calculator")
    PORT = os.getenv("DB_PORT", "5432")
    TEST_NAME = os.getenv("TEST_DB_NAME", "test_finance_calculator")


class GeneralConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
    DEBUG = bool(int(os.getenv("DEBUG", 0)))
    CORS_ORIGIN_ALLOW_ALL = bool(int(os.getenv("CORS_ORIGIN_ALLOW_ALL", 0)))
    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "Europe/Warsaw"
    STATIC_URL = "static/"


general_config = GeneralConfig()
db_config = DBConfig()
