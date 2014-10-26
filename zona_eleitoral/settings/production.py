from zona_eleitoral.base_settings import *

MY_APPS = (
    'core',
    'eleicao',
    'acesso',
    'veiculos',
    'django_extensions',
    'south',
    'webodt',
    'jquery',
    'staticfiles_select2',
    'selectable',
    'selectable_select2',
    'dajaxice',
    'dajax',
    'apuracao',
)

INSTALLED_APPS = INSTALLED_APPS + MY_APPS

WEBODT_CONVERTER = 'webodt.converters.abiword.AbiwordODFConverter'
WEBODT_ODF_TEMPLATE_PREPROCESSORS = (
    'webodt.preprocessors.xmlfor_preprocessor',
    'webodt.preprocessors.unescape_templatetags_preprocessor'
)

WEBODT_TEMPLATE_PATH = LOCAL('odt_templates')
WEBODT_GOOGLEDOCS_EMAIL = 'usuariozon029@gmail.com'
WEBODT_GOOGLEDOCS_PASSWORD = 'Zon@0029'

SELECTABLE_ESCAPED_KEYS = ('label', 'value')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)

#AUTH_USER_MODEL = 'acesso.Usuario'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'NAME': 'db_zona_eleitoral2',
        'USER': 'zona_eleitoral',
        'PASSWORD': 'swordfish0001'
    }
}

APURACAO_PATH = '/var/web/zona_eleitoral/media/dados_apuracao/2014/divulgacao/oficial/%d/distribuicao/br'
APURACAO_XML_LOCAIS = 'br-0000-e00%d1-f002'
APURACAO_XML_ABRANGENCIA = 'br-0000-e00%d1-v'

LOGIN_URL = 'acesso:login'
LOGIN_REDIRECT_URL='home'
AUTHENTICATION_BACKENDS = ('acesso.backends.OrgaoBackend',
                           'django.contrib.auth.backends.ModelBackend',
                           )

ALLOWED_HOSTS = ['*']
DEBUG = False

TEMPLATE_DEBUG = DEBUG
