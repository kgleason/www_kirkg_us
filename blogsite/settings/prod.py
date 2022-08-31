from blogsite.settings.base import *
import environ

env = environ.env()
environ.Env.read_env()

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

SECRET_KEY = env('SECRET_KEY')