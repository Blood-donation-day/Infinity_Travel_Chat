from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()
env = os.environ.get

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = env("SECRET_KEY")
REDIS = env("REDIS") == "True"
DEBUG = env("DEBUG") == "True"
DATABASE = env("DATABASE") == "True"

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "daphne",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "corsheaders",
    "django_extensions",
    "chat",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "infinity_travel.urls"

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

WSGI_APPLICATION = "infinity_travel.wsgi.application"
ASGI_APPLICATION = "infinity_travel.asgi.application"


if REDIS:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [
                    {
                        "host": env("REDIS_CLOUD_HOST"),
                        "port": env("REDIS_CLOUD_PORT"),
                        "password": env("REDIS_CLOUD_PASSWORD")
                        # "host": env('REDIS_CLOUD_HOST'),
                        # "port": env('REDIS_CLOUD_PORT') or 6379,
                    }
                ],
            },
        },
    }
else:
    CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": "5432",
    },
    "chat": {
        "ENGINE": "djongo",
        "ENFORCE_SCHEMA": False,
        "NAME": env("MONGO_DB_NAME"),
        "LOGGING": {
            "version": 1,
            "loggers": {
                "djongo": {
                    "level": "DEBUG",
                    "propogate": False,
                }
            },
        },
        "CLIENT": {
            "host": env("MONGO_DB_HOST"),
            "port": int(env("MONGO_DB_PORT")),
            "username": env("MONGO_DB_USERNAME"),
            "password": env("MONGO_DB_PASSWORD"),
        },
    },
}

DATABASE_ROUTERS = ["infinity_travel.dbrouter.MultiDBRouter"]

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "core.permissions.JWTCookieAuthenticated",  # 쿠키값으로 인증
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 'rest_framework.permissions.AllowAny', # 누구나 접근
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # 인증된 사용자만 접근
        # 'rest_framework.permissions.IsAdminUser', # 관리자만 접근
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# 배포 시 설정변경
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True  # <-쿠키가 cross-site HTTP 요청에 포함될 수 있다

SPECTACULAR_SETTINGS = {
    "TITLE": "InfinifyTravel Project API Document",
    # "CONTACT": {
    #     "name": "김창환",
    #     "url": "https://github.com/Blood-donation-day",
    #     "email": "98susckdghks@naver.com",
    # },
    "VERSION": "1.0.0",
}


EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
