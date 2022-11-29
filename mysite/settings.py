from __future__ import absolute_import, unicode_literals
import os, ssl
from pathlib import Path
from celery.schedules import crontab
from .celery import app as celery_app


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "^6&e1y71+2go2%15c$&kzi4=^n_lotvo4v%bb7#6cve3ja=qs0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DISABLE_SSL = True # Set this to True for local changes, but make sure to set back to False before commiting local changes to git!!

USE_S3 = os.getenv('USE_S3') == 'TRUE'

ALLOWED_HOSTS = ['localhost','127.0.0.1','project-b13.herokuapp.com']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

#SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SECURE_HSTS_SECONDS = 60

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

# Application definition
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS = [
    'channels',
    'bootstrap5',
    "studybuddy.apps.StudybuddyConfig",
    'ChatApp.apps.ChatappConfig',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'allauth',
    'celery',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    'crispy_bootstrap5',
    'storages',
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

ROOT_URLCONF = "mysite.urls"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

CSRF_TRUSTED_ORIGINS = ["https://project-b13.herokuapp.com"]

#changes to here and staticfiles_dirs were to allow static images
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'studybuddy', 'templates'), os.path.join(BASE_DIR, 'ChatApp', 'templates')], #previously [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = "mysite.wsgi.application"
ASGI_APPLICATION = 'mysite.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'damtdnjkuaauft',
        'USER': 'iqbbywpfszpkup',
        'PASSWORD': '26280677f952b1848483c33a6103d2af008a6b9a1884547e0bbde59fb6233a66',
        'HOST': 'ec2-44-207-253-50.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/




if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Needed to add this for google authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]


# Additional configuration settings
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGOUT_ON_GET= True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_LOGIN_ON_GET=True


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = "America/New_York"
CELERY_BEAT_SCHEDULE = {
    'task1': {
        'task': 'studybuddy.tasks.updateClassesDB',
        'schedule': crontab(minute=59, hour=23)
    }
}


ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False

heroku_redis_ssl_host = {
    'address': 'rediss://:p651279d43c25973a3bb50fe380280f2d3ce2d3c6e313befb483abfc0090418fe@ec2-52-21-235-5.compute-1.amazonaws.com:10480/0',  # The 'rediss' schema denotes a SSL connection.
    'ssl': ssl_context
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
                  "hosts": (heroku_redis_ssl_host, )
                  #"symmetric_encryption_keys": [SECRET_KEY],
         },
        
   }
}

try:
    if 'HEROKU' in os.environ:
        import django_heroku
        django_heroku.settings(locals())
except ImportError:
    found = False
    
    
# Override production variables if DJANGO_DEVELOPMENT env variable is true
if DISABLE_SSL:
    
    SECURE_SSL_REDIRECT = False
    
    SESSION_COOKIE_SECURE = False

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    CSRF_COOKIE_SECURE = False
    
    SECURE_HSTS_SECONDS = 0

    SECURE_HSTS_INCLUDE_SUBDOMAINS = False

    SECURE_HSTS_PRELOAD = False

   
