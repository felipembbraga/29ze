#-*- coding: utf-8 -*-
__author__ = 'felipe'

from django import template
from django.template import Library
from veiculos.models import PerfilVeiculo, Alocacao
from eleicao.models import LocalVotacao, Equipe

register = Library()

@register.simple_tag
def total_veiculos( perfil, equipe, local=None):
    qs = Alocacao.objects.filter(perfil_veiculo=perfil, equipe=equipe)
    if local:
        qs = qs.filter(local_votacao=local)
    if qs.exists():
        alocacao = qs[0]
        return alocacao.quantidade
    return u'sem número'

