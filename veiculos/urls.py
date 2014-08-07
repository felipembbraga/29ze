'''
Created on 05/08/2014

@author: felipe
'''
from django.conf.urls import include, url, patterns
from views import index, veiculo_index, veiculo_cadastrar, veiculo_editar, veiculo_ajax_get_modelo, info
from veiculos.views import veiculo_excluir

veiculo_patterns = [
    url(r'^cadastrar/$', veiculo_cadastrar, name='cadastrar'),
    url(r'^editar/(\d+)/$', veiculo_editar, name='editar'),
    url(r'^get-modelos/(\d+)/$', veiculo_ajax_get_modelo, name='ajax_get_modelo'),
    url(r'^excluir/(\d+)/$', veiculo_excluir, name='excluir'),
    url(r'^index/$', veiculo_index, name='index'),
]



urlpatterns = patterns('',
    url(r'^index/$',index, name='veiculos_index' ),
    url(r'^info/$',info, name='veiculos_info' ),
    url(r'^veiculo/',include(veiculo_patterns, namespace='veiculo')),
    
)