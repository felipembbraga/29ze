'''
Created on 05/08/2014

@author: felipe
'''
from django.conf.urls import include, url, patterns
from veiculos.views_relatorio import relatorio_veiculos, relatorio_admin_orgao_sem_veiculo, \
    relatorio_veiculos_requisitados

from views import index, veiculo_index, veiculo_cadastrar, veiculo_editar, veiculo_ajax_get_modelo, info
from veiculos.views import veiculo_excluir, veiculo_listar, veiculo_requisitar, veiculo_liberar, veiculo_detalhar, \
    perfil_veiculo_cadastrar, perfil_veiculo_listar, perfil_veiculo_editar, perfil_veiculo_detalhar, \
    cronograma_cadastrar, cronograma_editar, cronograma_excluir


veiculo_patterns = [
    url(r'^cadastrar/$', veiculo_cadastrar, name='cadastrar'),
    url(r'^editar/(\d+)/$', veiculo_editar, name='editar'),
    url(r'^get-modelos/(\d+)/$', veiculo_ajax_get_modelo, name='ajax_get_modelo'),
    url(r'^excluir/(\d+)/$', veiculo_excluir, name='excluir'),
    url(r'^listar/$', veiculo_listar, name='listar'),
    url(r'^listar/(\d+)/$', veiculo_listar, name='listar'),
    url(r'^detalhar/(\d+)/$', veiculo_detalhar, name='detalhar'),
    url(r'^requisitar/(\d+)/$', veiculo_requisitar, name='requisitar'),
    url(r'^liberar/(\d+)/$', veiculo_liberar, name='liberar'),
    url(r'^index/$', veiculo_index, name='index'),
]

perfil_veiculo_patterns = [
    url(r'^cadastrar/$', perfil_veiculo_cadastrar, name='cadastrar'),
    url(r'^editar/(\d+)/$', perfil_veiculo_editar, name='editar'),
    url(r'^excluir/(\d+)/$', veiculo_excluir, name='excluir'),
    url(r'^listar/$', perfil_veiculo_listar, name='listar'),
    url(r'^detalhar/(\d+)/$', perfil_veiculo_detalhar, name='detalhar'),
]

cronograma_veiculo_patterns = [
    url(r'^cadastrar/(\d+)/$', cronograma_cadastrar, name='cadastrar'),
    url(r'^editar/(\d+)/$', cronograma_editar, name='editar'),
    url(r'^excluir/(\d+)/$', cronograma_excluir, name='excluir'),
    ]

report_patterns = [
    url(r'^veiculos/$', relatorio_veiculos, name='veiculos'),
    url(r'^orgaos-sem-veiculos/$', relatorio_admin_orgao_sem_veiculo, name='orgaos-sem-veiculos'),
    url(r'^veiculos-requisitados/$', relatorio_veiculos_requisitados, name='veiculos-requisitados'),
    url(r'^veiculos-requisitados/(\d+)/$', relatorio_veiculos_requisitados, name='veiculos-requisitados'),
]

urlpatterns = patterns('',
                       url(r'^index/$', index, name='veiculos_index'),
                       url(r'^info/$', info, name='veiculos_info'),
                       url(r'^veiculo/', include(veiculo_patterns, namespace='veiculo')),
                       url(r'^perfil-veiculo/', include(perfil_veiculo_patterns, namespace='perfil-veiculo')),
                       url(r'^cronograma/', include(cronograma_veiculo_patterns, namespace='cronograma-veiculo')),
                       url(r'^report/', include(report_patterns, namespace='report-veiculos')),

)