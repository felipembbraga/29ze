from apuracao.views import monitorar_apuracao
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^monitorar/$', monitorar_apuracao, name='monitorar'),
)