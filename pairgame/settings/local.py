from celery.schedules import crontab

from .base import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# REST Framework configuration

REST_FRAMEWORK_DEFAULT_RENDERER_CLASSES.append(
    'rest_framework.renderers.BrowsableAPIRenderer'
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': REST_FRAMEWORK_DEFAULT_RENDERER_CLASSES,
    'DEFAULT_PERMISSION_CLASSES': REST_FRAMEWORK_DEFAULT_PERMISSION_CLASSES,
    'DEFAULT_AUTHENTICATION_CLASSES': REST_FRAMEWORK_DEFAULT_AUTHENTICATION_CLASSES
}

# Celery

CELERY_BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = 'redis://'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'America/Bogota'
CELERY_BEAT_SCHEDULE = {
    'scraping': {
        'task': 'worlds.tasks.scraping',
        'schedule': crontab()
    }
}