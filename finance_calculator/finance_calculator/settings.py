from pathlib import Path

from finance_calculator.config import db_config, general_config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = general_config.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = general_config.DEBUG

ALLOWED_HOSTS = general_config.ALLOWED_HOSTS
CORS_ORIGIN_ALLOW_ALL = general_config.CORS_ORIGIN_ALLOW_ALL

# Application definition
INSTALLED_APPS = [
    # Extensions
    "rest_framework",
    "corsheaders",
    # Custom
    "loan_calculator",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "finance_calculator.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "finance_calculator.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": db_config.NAME,
        "USER": db_config.USER,
        "PASSWORD": db_config.PWD,
        "HOST": db_config.HOST,
        "PORT": db_config.PORT,
        "TEST": {
            "NAME": db_config.TEST_NAME,
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = general_config.LANGUAGE_CODE

TIME_ZONE = general_config.TIME_ZONE

STATIC_URL = general_config.STATIC_URL

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
