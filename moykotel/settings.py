"""
Django settings for moykotel moykotel.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from decouple import config

# Build paths inside the moykotel like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "modeltranslation",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",

    "moykotel",
    "fpages",
    "accounts",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.yandex",
    "reset_migrations",
    "django_apscheduler",
    "newsletters",
]

SITE_ID = 2

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    'moykotel.middlewares.TimezoneMiddleware',
]

ROOT_URLCONF = "moykotel.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = "moykotel.wsgi.application"

LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Русский')
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }

    # "default": {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'postgres',
    #     'USER': 'postgres',
    #     'PASSWORD': '',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# присоединяем CSS
STATICFILES_DIRS = [BASE_DIR / 'static']

SITE_URL = 'http://127.0.0.1:8000'

LOGIN_REDIRECT_URL = '/news'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_FORMS = {'signup': 'accounts.forms.CustomSignupForm'}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

EMAIL_SUBJECT_PREFIX = '[MoyKotel] '

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

MANAGERS = (
    ('Manager', 'kulstas@gmail.com	'),
)

ADMINS = (
    ('Admin', 'kulagin@alltrade.biz'),
)

APSCHEDULER_DATETIME_FORMAT = 'N j, Y, f:s a'
APSCHEDULER_RUN_NOW_TIMEOUT = 25

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        'TIMEOUT': 300,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
        'warning': {
            'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s'
        },
        'error': {
            'format': '%(asctime)s %(levelname)s %(message)s %(exc_info)s'
        },
        'file_mod': {
            'format': '%(asctime)s %(levelname)s %(module)s'
        },
        'file_dump': {
            'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s %(exc_info)s'
        },
        'file_sec': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console_debug': {
            'level': 'CRITICAL',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': "simple"
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': "warning"
        },
        'console_error': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': "error"
        },
        "file_general": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.FileHandler",
            "filename": "general.log",
            'formatter': "file_mod"
        },
        "file_errors": {
            "level": "CRITICAL",
            "class": "logging.FileHandler",
            "filename": "errors.log",
            'formatter': "file_dump"
        },
        "file_sec": {
            "class": "logging.FileHandler",
            "filename": "security.log",
            'formatter': "file_sec"
        },
        'mail_admins': {
            'level': 'ERROR',
            "filters": ["require_debug_false"],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'warning'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console_debug', 'console_warning', 'console_error'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['file_errors', 'mail_admins'],
        },
        'django.template': {
            'handlers': ['file_errors'],
        },
        'django.db.backends': {
            'handlers': ['file_errors'],
        },
        'django.security': {
            'handlers': ['file_sec'],
        }
    }
}