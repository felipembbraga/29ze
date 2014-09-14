from django.conf.urls import url, patterns, include
from views import *

local_patterns = [
    url(r'^listar/$', local_listar, name='listar'),
    url(r'^cadastrar/$', local_cadastrar, name='cadastrar'),
]

urlpatterns = patterns('',
    url(r'^veiculos/importar/carro/$',carro_importar, name='importar_fipe' ),
    url(r'^veiculos/importar/caminhao/$',caminhao_importar, name='importar_fipe_caminhao' ),
    url(r'^local/', include(local_patterns, namespace='local-core')),    
)