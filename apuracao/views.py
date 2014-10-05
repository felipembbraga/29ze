#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.template.context import RequestContext
from eleicao.models import Equipe
from django.db import models


@login_required
@permission_required('veiculos.monitor_vistoria', raise_exception=True)
def monitorar_apuracao(request):
    return render(request, 'apuracao/monitor-apuracao.html', RequestContext(request, {'lista_cidades': monta_monitoramento(request)}))


def monta_monitoramento(request):
    cidades = Equipe.objects.all().select_related()
    lista_cidades = []
    for cidade in cidades:

        if cidade.equipesalocacao_set.all():
            percentual = (100 * cidade.equipesalocacao_set.first().veiculos_alocados) / cidade.equipesalocacao_set.first().total_estimativa

            if percentual <= 25:
                progress = 'danger'
            elif percentual <= 50:
                progress = 'warning'
            elif percentual <= 75:
                progress = 'ingo'
            else:
                progress = 'success'

            dict = {'cidade': cidade,
                    'total': cidade.equipesalocacao_set.first().total_estimativa,
                    'sessoes_restantes': cidade.equipesalocacao_set.first().total_estimativa - cidade.equipesalocacao_set.first().veiculos_alocados,
                    'sessoes_apuradas': cidade.equipesalocacao_set.first().veiculos_alocados,
                    'percentual': percentual,
                    'progress': progress}
        else:
            dict = {'cidade': cidade,
                    'total': cidade.alocacao_set.aggregate(models.Sum('quantidade')).get('quantidade__sum'),
                    'sessoes_restantes': 0,
                    'sessoes_apuradas': cidade.veiculoalocado_set.count(),
                    'percentual': 100,
                    'progress': 'success'}

        lista_cidades.append(dict)

    return lista_cidades
