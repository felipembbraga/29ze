'''
Created on 05/08/2014

@author: felipe
'''
from django.conf.urls import include, url, patterns
from views import index, veiculo_cadastrar

veiculo_patterns = [
    url(r'^cadastrar/$', veiculo_cadastrar, name='cadastrar'),
    #url(r'^editar/(\d+)/$', eleicao_editar, name='editar'),
    #url(r'^index/$', eleicao_index, name='index'),
]

urlpatterns = patterns('',
    url(r'^index/$',index, name='index' ),
    url(r'^veiculo/',include(veiculo_patterns, namespace='veiculo')),
    
)