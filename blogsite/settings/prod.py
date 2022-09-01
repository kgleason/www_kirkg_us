from blogsite.settings.base import *
import environ

env = environ.Env()
environ.Env.read_env()

DEBUG = False

ALLOWED_HOSTS = ['kirkg.us', '.kirkg.us', '127.0.0.1', '::1',  ]

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

CSRF_TRUSTED_ORIGINS = ['https://kirkg.us', 'https://www.kirkg.us', 'http://127.0.0.1', 'http://[::1]', ]

STATIC_ROOT = "/opt/django/static"
