"""
Django settings for DCR project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-n2j07y-lyf&z6o-t3a+hz&kr(9bp6fqxryjey$tij1gi3x=80d"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS=['https://api.easesfa.com']


# Application definition
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
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "phonenumber_field",
    "corsheaders",
    "django.contrib.postgres",
    "rest_fuzzysearch",
    "drf_multiple_model",
    "django_filters",
    "rest_framework_simplejwt.token_blacklist",
    "nepali_datetime_field",
    # 'query_counter',
    # 'debug_toolbar',
    "Company",
    "Chemist",
    "Doctors",
    "Expenses",
    "Mpo",
    "Payment",
    "Product",
    "Stockist",
    "DCRUser",
    "Account",
    "dailycallrecord",
    "helpandsupport",
    "dummy",
    "Notifications",
    "otherroles",
    "chat",
    "Stat",
    "sales",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # 'query_counter.middleware.DjangoQueryCounterMiddleware',
]
# CORS_ALLOWED_ORIGINS = [
#     "http://192.168.1.70:8000",
#     "https://example.com",
#     "https://sub.example.com",
#     "http://localhost:3000",
#     "http://127.0.0.1:9000",
#     "https://7c36-110-44-115-245.ngrok-free.app/"
# ]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = "DCR.urls"

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

# WSGI_APPLICATION = 'DCR.wsgi.application'
ASGI_APPLICATION = "DCR.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'dcr',
#         'USER': 'postgres',
#         'HOST': 'localhost',
#         'PASSWORD': 'password',
#         'PORT': '5432',

#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "dcr",
        "USER": "postgres",
        "HOST": "159.65.145.104",
        "PASSWORD": "password",
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "Account.User"


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# media files configuration
# Base url to serve media files
MEDIA_URL = "/media/"
# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


# Simple JWT configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=120),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    # 'UPDATE_LAST_LOGIN': False,
    # 'ALGORITHM': 'HS256',
    # 'SIGNING_KEY': SECRET_KEY,
    # 'VERIFYING_KEY': None,
    # 'AUDIENCE': None,
    # 'ISSUER': None,
    # 'JWK_URL': None,
    # 'LEEWAY': 0,
    # 'AUTH_HEADER_TYPES': ('Bearer',),
    # 'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    # 'USER_ID_FIELD': 'id',
    # 'USER_ID_CLAIM': 'user_id',
    # 'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    # 'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    # 'TOKEN_TYPE_CLAIM': 'token_type',
    # 'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    # 'JTI_CLAIM': 'jti',
    # 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    # 'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# the reset token is valid for 900 second only so that the reset password link will be valid for 900 seconds
PASSWORD_RESET_TIMEOUT = 900

# email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "te96476@gmail.com"
EMAIL_HOST_PASSWORD = "qsnrtbpfudnqkusf"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# EMAIL_PAGE_DOMAIN = 'https://mydomain.com/'

# SECRET_KEY = config('SECRET_KEY')

# Filter Configuration
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# INTERNAL_IPS = [
#     # ...
#     "127.0.0.1",
#     # ...
# ]

# cache configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# Date configuration
# REST_FRAMEWORK = {
#     'DATE_INPUT_FORMATS': ['iso-8601', '%Y-%m-%dT%H:%M:%S.%fZ'],
# }


# django channels layer configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# {
#     'DQC_SLOWEST_COUNT': 5,
#     'DQC_TABULATE_FMT': 'pretty',
#     'DQC_SLOW_THRESHOLD': 1,  # seconds
#     'DQC_INDENT_SQL': True,
#     'DQC_PYGMENTS_STYLE': 'tango',
#     'DQC_PRINT_ALL_QUERIES': True,
#     'DQC_COUNT_QTY_MAP': {
#         5: 'green',
#         10: 'white',
#         20: 'yellow',
#         30: 'red',
#     },
# }
