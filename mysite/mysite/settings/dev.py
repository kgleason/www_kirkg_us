from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-lxi#29l@&!o5@9)a6%m%05c3@ug=fc0donssvmxmld54@4e+-k"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mysite',
        'USER': 'wagtail',
        'PASSWORD': 'hz_qhjhwdxmwzrJso-RPdW-aAzoyTBiirgBBVGqxi@WyBiDg4xtPu7Vfs*kqwxwTsZXbKPfsZouWNTmuXpQRaUR.nzu@oX_Lg-Mr',
        'HOST': 'localhost',  # Use '127.0.0.1' or your database server's IP
        'PORT': '5432',       # Default PostgreSQL port
    }
}

try:
    from .local import *
except ImportError:
    pass
