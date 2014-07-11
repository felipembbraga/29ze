from django.conf.urls import include, url, patterns
from views import eleicao_cadastrar, eleicao_editar,\
     eleicao_index, local_importar, local_index

eleicao_patterns = [
    url(r'^cadastrar/$', eleicao_cadastrar, name='cadastrar'),
    url(r'^editar/(\d+)/$', eleicao_editar, name='editar'),
    url(r'^index/$', eleicao_index, name='index'),
]

local_votacao_patterns = [
    url(r'^index/$', local_index, name='index'),
    url(r'^importar/$', local_importar, name='importar'),
]

urlpatterns = patterns('',
    url(r'^eleicao/', include(eleicao_patterns, namespace='eleicao')),
    url(r'^locais/', include(local_votacao_patterns, namespace='local')),
)
