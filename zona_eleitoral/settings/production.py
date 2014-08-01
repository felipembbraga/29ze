from zona_eleitoral.base_settings import *

MY_APPS = (
    'core',
    'eleicao',
    'equipe'
)

INSTALLED_APPS = INSTALLED_APPS + MY_APPS

#AUTH_USER_MODEL = 'acesso.Usuario'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'NAME': 'db_zona_eleitoral',
        'USER': 'zona_eleitoral',
        'PASSWORD': 'swordfish0001'
    }
}
ALLOWED_HOSTS = ['*']
DEBUG = True

TEMPLATE_DEBUG = True
