"""
Django settings for zona_eleitoral project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOCAL = lambda x: os.path.join(BASE_DIR, x)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd4zg)@#iq%a)r5a$dja*06n)=7(=k19ep+k1wzu0_^k5wv^4c('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
SESSION_COOKIE_AGE = 86400

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'eleicao.middleware.EleicaoMiddleware',
    'eleicao.middleware.FormAgregarSecaoMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
"eleicao.context_processors.eleicao_atual",
"zona_eleitoral.context_processors.base_url")

ROOT_URLCONF = 'zona_eleitoral.urls'

WSGI_APPLICATION = 'zona_eleitoral.deploy.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

DATE_FORMAT= '%d/%m/%Y'

USE_I18N = True

USE_L10N = True

NUMBER_GROUPING = 3

USE_THOUSAND_SEPARATOR = True

THOUSAND_SEPARATOR = '.'

DECIMAL_SEPARATOR = ','

USE_TZ = True

from django.contrib import messages

MESSAGE_TAGS = {messages.DEBUG: 'debug',
messages.INFO: 'info',
messages.SUCCESS: 'success',
messages.WARNING: 'warning',
messages.ERROR: 'danger'}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = LOCAL('media')

STATIC_ROOT = LOCAL('static')

TEMPLATE_DIRS = (
    LOCAL('templates'),
)
