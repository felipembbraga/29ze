from zona_eleitoral.base_settings import *

MY_APPS = (
    'core',
    'eleicao',
    'acesso',
    'veiculos',
    'django_extensions',
    'south'
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
        'NAME': 'db_zona_eleitoral_dev',
        'USER': 'zona_eleitoral_dev',
        'PASSWORD': 'qwerasdf'
    }
}

LOGIN_URL = 'acesso:login'
LOGIN_REDIRECT_URL='home'
AUTHENTICATION_BACKENDS = ('acesso.backends.OrgaoBackend',
                           'django.contrib.auth.backends.ModelBackend',
                           )

WSGI_APPLICATION = 'zona_eleitoral.deploy.wsgi-dev.application'

try:
    from development_local import *
except:
    pass