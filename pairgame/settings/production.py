import dj_database_url
from celery.schedules import crontab

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}

# REST Framework configuration

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': REST_FRAMEWORK_DEFAULT_RENDERER_CLASSES,
    'DEFAULT_PERMISSION_CLASSES': REST_FRAMEWORK_DEFAULT_PERMISSION_CLASSES,
    'DEFAULT_AUTHENTICATION_CLASSES': REST_FRAMEWORK_DEFAULT_AUTHENTICATION_CLASSES
}

# Celery

CELERY_BROKER_URL = os.environ["REDIS_URL"]
CELERY_RESULT_BACKEND = os.environ["REDIS_URL"]
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'America/Bogota'
CELERY_BEAT_SCHEDULE = {
    'scraping': {
        'task': 'worlds.tasks.scraping',
        'schedule': crontab(hour=19, minute=51)
    }
}