#-*- coding: utf-8 -*-
from datetime import datetime
from apuracao.views import monta_monitoramento
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils import timezone
from veiculos.ajax import process_modal


@dajaxice_register()
def recarregar_monitoramento(request):
    """
    Atualiza o select dos modelos de acordo com a marca selecionada
    """
    dajax = Dajax()
    if request.is_ajax():
        try:
            monitoramento = monta_monitoramento(request)
            data_padrao = timezone.make_aware(datetime(1900, 01, 01), timezone.get_default_timezone())
            render = render_to_string('apuracao/monitor-detalhe-apuracao.html', RequestContext(request, {'lista_cidades': monitoramento, 'data_padrao': data_padrao}))
            dajax.assign('#monitor-detalhe', 'innerHTML', render)
        except Exception, e:
            dajax = process_modal(dajax, 'msg',
                                  "Ocorreu um erro: <strong>%s</strong><br>Favor entrar em contato com o departamento de TI." % e,
                                  True)
    else:
        dajax = process_modal(dajax, 'msg', u"Instrução inválida!", True)
    return dajax.json()
