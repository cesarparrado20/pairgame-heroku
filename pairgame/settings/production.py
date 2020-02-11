import dj_database_url

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