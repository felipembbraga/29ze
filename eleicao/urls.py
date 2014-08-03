from django.conf.urls import include, url, patterns
from views import *

from views_relatorio import *
eleicao_patterns = [
    url(r'^cadastrar/$', eleicao_cadastrar, name='cadastrar'),
    url(r'^editar/(\d+)/$', eleicao_editar, name='editar'),
    url(r'^index/$', eleicao_index, name='index'),
]

local_votacao_patterns = [
    url(r'^$', local_index, name='index'),
    url(r'^importar/$', local_importar, name='importar'),
    url(r'^detalhar/(\d+)/$', local_detalhar, name='detalhar'),
    url(r'^definir-equipe/(\d+)/$', local_definir_equipe, name='definir-equipe'),
]

secao_patterns = [
    url(r'^agregar/$', secao_agregar, name='agregar'),
    url(r'^agregar-externo/(\d+)/$', secao_agregar_externo, name='agregar-externo'),
    url(r'^selecionar-secoes/(\d+)/$', secao_selecionar_secoes, name='selecionar-secoes'),
    url(r'^desagregar/(\d+)/$', secao_desagregar, name='desagregar'),
]

equipe_patterns = [
    url(r'^$', equipe_index, name='index'),
    url(r'^cadastrar/$', equipe_cadastrar, name='cadastrar'),
    url(r'^editar/(\d+)/$', equipe_editar, name='editar'),
    url(r'^excluir/(\d+)/$', equipe_excluir, name='excluir'),
    url(r'^detalhar/(\d+)/$', equipe_detalhar, name='detalhar'),
    url(r'^selecionar-locais/(\d+)/$', equipe_selecionar_locais, name='selecionar-locais'),
]

reports_patterns = [
    url(r'^local-geral/$', relatorio_local_geral, name='local-geral'),
    url(r'^local-equipe/$', relatorio_local_equipe, name='local-equipe'),
    url(r'^local-mala-direta/$', relatorio_local_mala_direta, name='local-mala-direta'),
    url(r'^secao-ordenado/$', relatorio_secao_ordenado, name='secao-ordenado'),
    url(r'^secao-ordenado-xls/$', relatorio_secao_ordenado_xls, name='secao-ordenado-xls'),
]


urlpatterns = patterns('',
    url(r'^eleicao/', include(eleicao_patterns, namespace='eleicao')),
    url(r'^locais/', include(local_votacao_patterns, namespace='local')),
    url(r'^secao/', include(secao_patterns, namespace='secao')),
    url(r'^equipe/', include(equipe_patterns, namespace='equipe')),
    url(r'^report/', include(reports_patterns, namespace='eleicao-report')),
    
)
