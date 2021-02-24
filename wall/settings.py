"""
Django settings for wall project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    "django_celery_results",
    'rest_framework',
    'corsheaders',
    "taggit",
    "geo",
    "votes",
    "predict",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "wall.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": ["templates/"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.i18n",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]
    },
}]

WSGI_APPLICATION = "wall.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("POSTGRES_DB", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("POSTGRES_USER", "user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "de"

LANGUAGES = [
    ("de", _("German")),
    ("fr", _("French")),
    ("it", _("Italian")),
    ("en", _("English")),
]

TIME_ZONE = "Europe/Zurich"

CELERY_TIMEZONE = TIME_ZONE

USE_I18N = True

LOCALE_PATHS = ["locale/"]

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = "static/"
STATIC_URL = "/static/"

MEDIA_ROOT = "media/"
MEDIA_URL = "/media/"

# Celery configuration

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "webmaster@localhost")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "root@localhost")

EMAIL_HOST = os.environ.get("SMTP_HOST", "smtp")
EMAIL_PORT = int(os.environ.get("SMTP_PORT", "25"))

EMAIL_USE_TLS = int(os.environ.get("SMTP_TLS", "0"))
EMAIL_USE_SSL = int(os.environ.get("SMTP_SSL", "0"))

EMAIL_HOST_USER = os.environ.get("SMTP_USER", "user")
EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASSWORD", "pw")

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "webmaster@localhost")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "root@localhost")

CELERY_BROKER_URL = "redis://redis:6379"

CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'cache:11211',
    }
}

if DEBUG:
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache',}}

JAZZMIN_SETTINGS = {
    "site_title": _("Magic Wall Admin"),
    "site_header": _("Magic Wall"),
    "site_logo": "logo.png",
    "welcome_sign": _("Magic Wall Admin"),
    "copyright": "",
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]}
    ],
    "usermenu_links": [],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [],
    "custom_links": {},
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "geo.Gemeinde": "fas fa-city",
        "geo.Kanton": "fas fa-map-pin",
        "predict.Result": "fas fa-vote-yea",
        "predict.LatestResult": "fas fa-clock",
        "predict.VotingModel": "fas fa-square-root-alt",
        "votes.Votation": "fas fa-fist-raised",
        "votes.VotationDate": "fas fa-calendar-day",
        "django_celery_beat.PeriodicTask": "fas fa-tasks",
        "django_celery_beat.ClockedSchedule": "fas fa-clock",
        "django_celery_beat.CrontabSchedule": "fas fa-clipboard-list",
        "django_celery_beat.IntervalSchedule": "fas fa-sync",
        "django_celery_beat.SolarSchedule": "fas fa-sun",
        "django_celery_results.TaskResult": "fas fa-flag-checkered",
        "taggit.Tag": "fas fa-tags",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_js": None,
    "show_ui_builder": False,
    "changeform_format_overrides": {"auth.group": "vertical_tabs"},
    "language_chooser": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-danger navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": "",
    "actions_sticky_top": True,
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_URLS_REGEX = r'^/api/.*$'
