#-*- coding: utf-8 -*-
from operator import itemgetter
from apuracao.models import importar_dados, Cidade
from dateutils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.template.context import RequestContext
from django.utils import timezone
from django.utils.datetime_safe import datetime
from eleicao.models import Equipe
from django.db import models


@login_required
@permission_required('veiculos.monitor_vistoria', raise_exception=True)
def monitorar_apuracao(request):
    return render(request, 'apuracao/monitor-apuracao.html', RequestContext(request, {'lista_cidades': monta_monitoramento(request)}))


def monta_monitoramento(request):
    cidades = importar_dados()
    lista_cidades = []

    for cidade in cidades:
        if cidade.apuracao_set.filter(turno=1).exists():
            apuracao = cidade.apuracao_set.filter(turno=1).order_by('-dt_atualizacao').first()

            if apuracao.percentual <= 25:
                progress = 'danger'
            elif apuracao.percentual <= 50:
                progress = 'warning'
            elif apuracao.percentual <= 75:
                progress = 'ingo'
            else:
                progress = 'success'

            dict = {'cidade': cidade,
                    'total': cidade.secoes,
                    'sessoes_restantes': apuracao.secoes_restantes,
                    'sessoes_apuradas': apuracao.secoes_totalizadas,
                    'percentual': apuracao.percentual,
                    'data_conclusao': apuracao.dt_finalizacao or timezone.make_aware(datetime(1900, 01, 01), timezone.get_default_timezone()),
                    'progress': progress}
        else:
            dict = {}

        lista_cidades.append(dict)

    return sorted(lista_cidades, key=itemgetter('data_conclusao', 'percentual'), reverse=True)
