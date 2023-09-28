from pathlib            import Path
from dj_database_url    import parse

import environ
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG", default = False)

ALLOWED_HOSTS = [
    '127.0.0.1',
    '.vercel.app',
    'localhost'
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "core",

    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "time_tracker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / 'time_tracker' / 'templates'
        ],
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

# debug_toolbar moved here. 
if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    INTERNAL_IPS = ['127.0.0.1', ]

    # this is the main reason for not showing up the toolbar
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': True,
    }


WSGI_APPLICATION = "time_tracker.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

def get_database():
    database_type = env("DATABASE_TYPE", default = "local").lower()
    
    if database_type in ["qa", "quality_assurance"]:
        return parse(env('DATABASE_URL_QA'))

    elif database_type in ["prod", "production"]:
        return parse(env('DATABASE_URL'))
    
    return {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }

DATABASES = {
    "default": get_database()
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL  = 'media/'

STATIC_ROOT = BASE_DIR / 'time_tracker' / 'static_cdn'
MEDIA_ROOT  = STATIC_ROOT / 'media'

ADMIN_MEDIA_URL = STATIC_URL + 'admin/' # admin is now served by staticfiles

STATICFILES_DIRS = [
    BASE_DIR / 'time_tracker' / STATIC_URL,
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"  # new

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
