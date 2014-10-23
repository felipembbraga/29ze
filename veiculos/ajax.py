# -*- coding: utf-8 -*-
import datetime
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from core.models import Modelo, Pessoa
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.template.loader import render_to_string
from eleicao.models import Equipe, EquipesAlocacao
from models import Veiculo, Motorista
from veiculos.autocomplete import equipes_c_vagas
from veiculos.forms import VeiculoVistoriaForm, VistoriaForm, MotoristaVistoriaForm, SelecaoVeiculoForm
from veiculos.models import VeiculoSelecionado, VeiculoAlocado
from django.db import models
from veiculos.views import monta_monitoramento


@dajaxice_register()
def requisicao_veiculo(request, id_veiculo, formulario):
    dajax = Dajax()
    try:
        veiculo = Veiculo.objects.get(pk=int(id_veiculo))
    except Exception, e:
        dajax.assign('#requisicao-veiculo-txt', 'innerHTML', 'Veiculo nao encontrado')
        return dajax.json()
    tem_pt = veiculo.veiculo_selecionado.filter(segundo_turno=False).exists()
    tem_st = veiculo.veiculo_selecionado.filter(segundo_turno=True).exists()
    if request.is_ajax():
        initial = {
            'id_veiculo': id_veiculo,
            'primeiro_turno': tem_pt,
            'segundo_turno': tem_st
        }

        if formulario:
            # Caso esteja sendo enviado o formulário
            formulario = deserialize_form(formulario)

            form = SelecaoVeiculoForm(formulario)
            if form.is_valid():
                if form.cleaned_data.get('primeiro_turno'):
                    if not tem_pt:
                        veiculo.veiculo_selecionado.create(veiculo=veiculo, segundo_turno=False)
                else:
                    if veiculo.veiculoalocado_set.filter(segundo_turno=False).exists():
                        dajax.script('$.notify({theme:"erro", title:"Veiculo ja alocado para primeiro turno!"});')
                        return dajax.json()
                    veiculo.veiculo_selecionado.filter(segundo_turno=False).delete()
                if form.cleaned_data.get('segundo_turno'):
                    if not tem_st:
                        veiculo.veiculo_selecionado.create(veiculo=veiculo, segundo_turno=True)
                else:
                    if veiculo.veiculoalocado_set.filter(segundo_turno=True).exists():
                        dajax.script('$.notify({theme:"sucesso", title:"Veiculo ja alocado"});')

                        return dajax.json()
                    veiculo.veiculo_selecionado.filter(segundo_turno=True).delete()
                dajax.script('location.reload();')
                return dajax.json()
        else:
            form = SelecaoVeiculoForm(initial=initial)
        render = render_to_string('veiculos/veiculo/requisicao_veiculo_form.html', {'form': form})
        dajax.assign('#requisicao-veiculo-txt', 'innerHTML', render)
    return dajax.json()


@dajaxice_register()
def consultar_veiculo(request, placa, turno):
    """
    Consulta um veículo para efetuar a vistoria
    - Caso não esteja cadastrado, o sistema dará a possibilidade de cadastro do veículo
    - Caso o veículo não tenha sido solicitado, pergunta se o servidor deseja solicitar o mesmo
    """
    dajax = Dajax()
    modal = None
    msg = ''

    if request.is_ajax():
        dajax = process_form_vistoria(dajax)
        try:
            if Veiculo.objects.filter(placa__iexact=placa, eleicao=request.eleicao_atual, veiculo_selecionado__isnull=False).exists() and \
                    Veiculo.objects.filter(placa__iexact=placa, eleicao=request.eleicao_atual, veiculo_selecionado__segundo_turno=turno).exists():
                # Caso o veículo exista no sistema
                veiculo = Veiculo.objects.get(placa__iexact=placa, eleicao=request.eleicao_atual)
                if veiculo.veiculoalocado_set.filter(segundo_turno=turno).exists():
                    if turno and datetime.date.today() > request.eleicao_atual.data_turno_2 or not turno and datetime.date.today() > request.eleicao_atual.data_turno_1:
                        msg = u'O veículo consultado já foi alocado!'
                        modal = 'msg'
                    else:
                        msg = u'O veículo consultado já foi alocado!<br>Desaloque o veículo para efetuar uma nova alocação ou consulte um novo veículo.'
                        modal = 'veiculo-alocado'
                        dajax.assign('#id_veiculo_alocado', 'value', veiculo.veiculoalocado_set.filter(segundo_turno=turno).first().id)
                else:
                    dajax = message_status(dajax, 'success', u"Veículo encontrado!", True)
                    dajax = process_form_vistoria(dajax, veiculo, True, request, segundo_turno=turno)
            elif (Veiculo.objects.filter(placa__iexact=placa, eleicao=request.eleicao_atual, veiculo_selecionado__isnull=True).exists() or
                    (Veiculo.objects.filter(placa__iexact=placa, eleicao=request.eleicao_atual) and
                        not Veiculo.objects.filter(placa__iexact=placa, eleicao=request.eleicao_atual, veiculo_selecionado__segundo_turno=turno).exists())):
                # Caso o veículo não tenha sido solicitado
                msg = u"O veículo solicitado ainda não foi requisitado, deseja requisitar?"
                modal = 'requisitar-veiculo'
            else:
                # Caso o veículo não tenha sido localizado no sistema
                msg = u"Veículo não encontrado!"
                modal = 'novo-veiculo'
        except Exception, e:
            msg = "Ocorreu um erro: <strong>%s</strong><br>Favor entrar em contato com o departamento de TI." % e
            modal = 'msg'
    else:
        msg = u"Instrução inválida!"
        modal = 'msg'

    if modal:
        dajax = message_status(dajax)
        dajax = process_form_vistoria(dajax)
        dajax = process_modal(dajax, modal, msg, True)
    else:
        dajax = process_modal(dajax, 'novo-veiculo')
        dajax = process_modal(dajax, 'requisitar-veiculo')
        dajax = process_modal(dajax, 'msg')

    return dajax.json()


@dajaxice_register()
def cadastrar_veiculo(request, placa, formulario, turno):
    """
    Caso não seja encontrado o veículo solicitado, possibilira cadastrá-lo diretamente na tela de vistoria
    """
    dajax = Dajax()

    if request.is_ajax():
        try:
            if formulario:
            # Caso esteja sendo enviado o formulário
                formulario = deserialize_form(formulario)
                if formulario.get('marca') != '':
                    VeiculoVistoriaForm.base_fields['modelo'].choices = [('', '---------')] + list(Modelo.objects.filter(marca__pk=int(formulario.get('marca'))).order_by('nome').values_list('pk', 'nome'))
                else:
                    VeiculoVistoriaForm.base_fields['modelo'].choices = [('', '---------')]

                v = Veiculo(eleicao=request.eleicao_atual)
                form = VeiculoVistoriaForm(formulario, instance=v)

                if form.is_valid():
                    # Se o formulário for válido
                    veiculo = form.save()
                    VeiculoSelecionado.objects.get_or_create(veiculo=veiculo, requisitado_vistoria=True,
                                                             segundo_turno=turno)  # realiza a requisição do veículo automaticamente

                    dajax = message_status(dajax, 'success', u"Veículo cadastrado com sucesso!", True)
                    dajax = process_form_vistoria(dajax, veiculo, True, request)
                    dajax = process_modal(dajax, 'add-veiculo')

                    return dajax.json()
            else:
                # Caso contrário, exibe o formulário em branco
                VeiculoVistoriaForm.base_fields['modelo'].choices = [('', '---------')]
                form = VeiculoVistoriaForm(initial={'placa': placa})

            render = render_to_string('veiculos/vistoria/add_veiculo_form.html', {'form': form})
            dajax = process_modal(dajax, 'add-veiculo', render, True)
        except Exception, e:
            dajax = process_modal(dajax, 'msg',
                                  "Ocorreu um erro: <strong>%s</strong><br>Favor entrar em contato com o departamento de TI." % e,
                                  True)
    else:
        dajax = process_modal(dajax, 'msg', u"Instrução inválida!", True)
    return dajax.json()


@dajaxice_register()
def change_marca(request, marca):
    """
    Atualiza o select dos modelos de acordo com a marca selecionada
    """
    dajax = Dajax()
    if request.is_ajax():
        try:
            modelos_filter = []
            modelos = ['<option value=''>---------</option>', ]

            if marca and marca != '':
                modelos_filter = Modelo.objects.filter(marca__pk=int(marca)).order_by('nome')

            for modelo in modelos_filter:
                modelos.append("<option value='%s'>%s</option>" % (modelo.pk, modelo.nome))

            dajax.assign('#id_modelo', 'innerHTML', ''.join(modelos))
        except Exception, e:
            dajax = process_modal(dajax, 'msg',
                                  "Ocorreu um erro: <strong>%s</strong><br>Favor entrar em contato com o departamento de TI." % e,
                                  True)
    else:
        dajax = process_modal(dajax, 'msg', u"Instrução inválida!", True)
    return dajax.json()


@dajaxice_register()
def requisitar_veiculo(request, placa, turno):
    """
    Requisita um veículo ainda não requisitado
    """
    dajax = Dajax()
    veiculo = Veiculo.objects.filter(placa__iexact=placa, eleicao=request.eleicao_atual)

    if veiculo:
        # Caso exista veículo com a placa informada no sistema, requisita o mesmo
        VeiculoSelecionado.objects.get_or_create(veiculo=veiculo.first(), requisitado_vistoria=True,
                                                 segundo_turno=turno)
        message = "Veículo requisitado com sucesso!"
        status = 'success'

        dajax = process_form_vistoria(dajax, veiculo.first(), True, request, segundo_turno=turno)
    else:
        message = "Veículo não encontrado!"
        status = 'danger'

    dajax = message_status(dajax, status, message, True)
    dajax = process_modal(dajax, 'requisitar-veiculo')
    return dajax.json()


def message_status(dajax, tipo=None, msg=None, exibe=False):
    """
    Monta o alert de acordo com o tipo de msg

    :param dajax: Objeto Dajax()
    :param tipo: tipo de alert que será exibido
    :param msg: conteúdo a ser inserido no alert
    :param exibe: insere ou remove o alert. True para inserir e False para remover
    :return: Objeto Dajax() processado
    """
    if exibe:
        message = """<div id="%(tipo)s-process" class="alert alert-%(tipo)s alert-dismissible" role="alert">
                        <button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                        <p>%(msg)s</p>
                     </div>""" % {'tipo': tipo, 'msg': msg}
        dajax.assign('#message-status', 'innerHTML', message)
        dajax.script("$('#message-status').show();")
    else:
        dajax.assign('#message-status', 'innerHTML', '')
        dajax.script("$('#message-status').hide();")
    return dajax


def process_modal(dajax, modal=None, msg=None, exibe=False, titulo=None):
    """
    Função utilizada para montar e exibir a seção do formulário de vistoria,
    ou esconder esta mesma seção de acordo com o parâmetro exibe

    :param dajax: Objeto Dajax()
    :param modal: o modal que deverá ser processado
    :param msg: conteúdo a ser inserido no modal
    :param exibe: exibe ou esconde o modal. True para exibir e False para esconder
    :return: Objeto Dajax() processado
    """
    if exibe:
        if titulo:
            dajax.assign('#modal-' + modal + '-title', 'innerHTML', msg)
        dajax.assign('#' + modal + '-txt', 'innerHTML', msg)
        dajax.script("$('#modal-" + modal + "').modal('show');")
    else:
        dajax.script("$('#modal-" + modal + "').modal('hide');")
        dajax.assign('#' + modal + '-txt', 'innerHTML', '')

    if titulo:
        dajax.assign('#modal-' + modal + '-title', 'innerHTML', titulo)

    return dajax


def process_form_vistoria(dajax, veiculo=None, exibe=False, request=None, form_vistoria=None, form_motorista=None, disable_show=False, segundo_turno=False):
    """
    Função utilizada para montar e exibir a seção do formulário de vistoria,
    ou esconder esta mesma seção de acordo com o parâmetro exibe

    :param dajax: Objeto Dajax()
    :param veiculo: instância do veículo a ser vistoriado
    :param exibe: exibe ou esconde a seção de vistoria. True para exibir e False para esconder
    :return: Objeto Dajax() processado
    """
    if exibe:
        if form_vistoria:
            form_vistoria = form_vistoria
        else:
            form_vistoria = VistoriaForm()

        if form_motorista:
            form_motorista = form_motorista
        elif veiculo.motorista_veiculo.all().exists():
            if segundo_turno and veiculo.motorista_veiculo.filter(~Q(segundo_turno=segundo_turno)).exists():
                motorista = veiculo.motorista_veiculo.filter(~Q(segundo_turno=segundo_turno)).first()
            else:
                motorista = veiculo.motorista_veiculo.filter(segundo_turno=segundo_turno).first()

            form_motorista = MotoristaVistoriaForm(initial={'motorista': motorista.pessoa,
                                                            'id': motorista.pessoa.id},
                                                   instance=motorista.pessoa)
        else:
            form_motorista = MotoristaVistoriaForm()

        if segundo_turno and veiculo.veiculoalocado_set.filter(segundo_turno=False).exists():
            veiculo_alocado = veiculo.veiculoalocado_set.filter(segundo_turno=False).first()
        else:
            veiculo_alocado = None

        render = render_to_string('veiculos/vistoria/vistoria_form.html', RequestContext(request,
                                                                                         {'veiculo': veiculo,
                                                                                          'veiculo_alocado': veiculo_alocado,
                                                                                          'form_vistoria': form_vistoria,
                                                                                          'form_motorista': form_motorista}))
        dajax.assign('#cadastrar-vistoria .panel-body', 'innerHTML', render)
        if not disable_show:
            dajax.script("$('#cadastrar-vistoria').show();")
    else:
        dajax.assign('#cadastrar-vistoria .panel-body', 'innerHTML', '')
        dajax.script("$('#cadastrar-vistoria').hide();")

    return dajax


@dajaxice_register()
def consulta_motorista(request, id_motorista, turno):
    """
    Preenche os campos do motorista com os dados encontrados no BD
    """
    dajax = Dajax()
    if request.is_ajax():
        try:

            if Motorista.objects.filter(pessoa__pk=int(id_motorista), eleicao=request.eleicao_atual,
                                        segundo_turno=turno).exists():
                motorista = Motorista.objects.get(pessoa__pk=int(id_motorista), eleicao=request.eleicao_atual,
                                                  segundo_turno=turno)
                if hasattr(motorista, 'veiculo') and motorista.veiculo and motorista.veiculo.veiculoalocado_set.filter(segundo_turno=turno).exists():
                    dajax = process_modal(dajax, 'msg',
                                          u'Não é possivel selecionar esse motorista. O mesmo se encontra vinculado a veículo já alocado.', True)
                    dajax.assign('#s2id_id_motorista span.select2-chosen', 'innerHTML', u'Selecione uma equipe')
                    dajax.script("$('#s2id_id_motorista').removeClass('select2-allowclear');")
                    dajax.script("$('#id_motorista').val('');")
                    return dajax.json()
                elif motorista.veiculo:
                    dajax = process_modal(dajax, 'requisitar-motorista',
                                          u'Motorista vinculado a outro veículo, deseja vincular a este?',
                                          True, u'Motorista vinculado a veículo')

                dajax.assign('#id_id', 'value', motorista.pessoa.id)
                dajax.assign('#id_titulo_eleitoral', 'value', motorista.pessoa.titulo_eleitoral)
                dajax.assign('#id_nome', 'value', motorista.pessoa.nome)
                dajax.assign('#id_endereco', 'value', motorista.pessoa.endereco)
            else:
                motorista = Pessoa.objects.get(pk=int(id_motorista))
                dajax.assign('#id_id', 'value', motorista.id)
                dajax.assign('#id_titulo_eleitoral', 'value', motorista.titulo_eleitoral)
                dajax.assign('#id_nome', 'value', motorista.nome)
                dajax.assign('#id_endereco', 'value', motorista.endereco)

        except Exception, e:
            dajax = process_modal(dajax, 'msg',
                                  "Ocorreu um erro: <strong>%s</strong><br>Favor entrar em contato com o departamento de TI." % e,
                                  True)
    else:
        dajax = process_modal(dajax, 'msg', u"Instrução inválida!", True)
    return dajax.json()


@dajaxice_register()
def cadastrar_vistoria(request, formulario, turno, alocacao_2_turno=None):
    """
    Efetua o cadastro da vistoria
    """
    dajax = Dajax()

    if request.is_ajax():
        try:
            if formulario:
                # Caso esteja sendo enviado o formulário
                form = deserialize_form(formulario)
                veiculo = Veiculo.objects.get(placa__iexact=form.get('placa_veiculo_vist'))
                if form.get('id'):
                    pessoa_motorista = Pessoa.objects.get(id=int(form.get('id')))
                    form_pessoa_motorista = MotoristaVistoriaForm(form, instance=pessoa_motorista)
                else:
                    form_pessoa_motorista = MotoristaVistoriaForm(form)
                form_vistoria = VistoriaForm(form)

                if form_pessoa_motorista.is_valid() and form_vistoria.is_valid():
                    # Se os formulários forem válidos
                    pessoa_motorista = form_pessoa_motorista.save()

                    if not Motorista.objects.filter(pessoa=pessoa_motorista,
                                                    eleicao=request.eleicao_atual, segundo_turno=turno).exists():
                        Motorista.objects.create(pessoa=pessoa_motorista, veiculo=veiculo,
                                                 eleicao=request.eleicao_atual, segundo_turno=turno)
                    else:
                        motorista = Motorista.objects.filter(pessoa=pessoa_motorista, eleicao=request.eleicao_atual,
                                                             segundo_turno=turno).first()
                        motorista.veiculo = veiculo
                        motorista.save()

                    alocacao_concluida = False
                    tipo_alocacao = form_vistoria.cleaned_data.get('alocacao')
                    cont = 0
                    while not alocacao_concluida:
                        cont += 1
                        if (tipo_alocacao == '0' and filter(equipes_c_vagas_locais, EquipesAlocacao.objects.filter(eleicao=request.eleicao_atual, segundo_turno=turno))) \
                                or (tipo_alocacao == '1' and filter(equipes_c_vagas, EquipesAlocacao.objects.filter(eleicao=request.eleicao_atual, segundo_turno=turno))):
                            if alocacao_2_turno is not None and not alocacao_2_turno and not form_vistoria.cleaned_data.get('alocacao_2_turno'):
                                veiculo_alocado = veiculo.veiculoalocado_set.filter(segundo_turno=False).first()
                                perfil = veiculo_alocado.perfil
                                equipe = veiculo_alocado.equipe
                                local_votacao = veiculo_alocado.local_votacao
                            else:
                                if tipo_alocacao == '0':
                                    import random

                                    # verifica se o servidor marcou o campo de alocação manual, e pega a equipe selecionada
                                    if form_vistoria.cleaned_data.get('alocacao_manual') and form_vistoria.cleaned_data.get('equipe_manual') is not None:
                                        equipe_auto = form_vistoria.cleaned_data.get('equipe_manual')
                                    else:
                                        equipe_auto = random.choice(filter(equipes_c_vagas_locais, EquipesAlocacao.objects.filter(eleicao=request.eleicao_atual, segundo_turno=turno).order_by('equipe__nome')))
                                    equipe_auto = equipe_auto.equipe

                                    # verifica se o servidor marcou o campo de alocação manual, e pega o local selecionado
                                    if form_vistoria.cleaned_data.get('alocacao_manual') and form_vistoria.cleaned_data.get('local_manual') is not None:
                                        local_auto = form_vistoria.cleaned_data.get('local_manual')
                                    else:
                                        local_auto = random.choice(filter(locais_c_vagas, equipe_auto.local_equipe.all()))

                                    # verifica se o servidor marcou o campo de alocação manual, e pega o perfil selecionado
                                    if form_vistoria.cleaned_data.get('alocacao_manual') and form_vistoria.cleaned_data.get('perfil_manual') is not None:
                                        alocacao = form_vistoria.cleaned_data.get('perfil_manual')
                                    else:
                                        alocacao = random.choice(filter(alocacao_c_vagas, local_auto.alocacao_set.filter(segundo_turno=turno)))

                                    perfil = alocacao.perfil_veiculo
                                    equipe = alocacao.equipe
                                    local_votacao = local_auto
                                else:
                                    perfil = form_vistoria.cleaned_data.get('perfil')
                                    equipe = form_vistoria.cleaned_data.get('equipe').equipe
                                    local_votacao = None

                            if (local_votacao and perfil in [perf.perfil_veiculo for perf in filter(alocacao_c_vagas, local_votacao.alocacao_set.filter(segundo_turno=turno))]) or \
                                    (local_votacao is None and EquipesAlocacao.objects.filter(equipe=equipe, eleicao=request.eleicao_atual, estimativa_equipe__gt=F('veiculos_alocados_equipe'), segundo_turno=turno)):
                                if not VeiculoAlocado.objects.filter(veiculo=veiculo, segundo_turno=turno).exists():
                                    veiculo_alocado = VeiculoAlocado.objects.create(veiculo=veiculo, perfil=perfil,
                                                                                    equipe=equipe,
                                                                                    local_votacao=local_votacao,
                                                                                    segundo_turno=turno)
                                else:
                                    veiculo_alocado = VeiculoAlocado.objects.get(veiculo=veiculo, segundo_turno=turno)
                                    veiculo_alocado.perfil = perfil
                                    veiculo_alocado.equipe = equipe
                                    veiculo_alocado.local_votacao = local_votacao
                                    veiculo_alocado.save()

                                alocacao_concluida = True
                            elif not form_vistoria.cleaned_data.get('alocacao_2_turno') or tipo_alocacao != '0' or form_vistoria.cleaned_data.get('alocacao_manual'):
                                dajax = process_modal(dajax, 'msg', u'Não existem vagas para a opção selecionada!', True)
                                dajax = process_form_vistoria(dajax)
                                if not form_vistoria.cleaned_data.get('alocacao_2_turno'):
                                    form_vistoria._errors["alocacao_2_turno"] = form_vistoria.error_class([u'Não existem vagas para a opção selecionada!'])
                                    del form_vistoria.cleaned_data["alocacao_2_turno"]
                                else:
                                    form_vistoria._errors["alocacao"] = form_vistoria.error_class([u'Não existem vagas para a opção selecionada!'])
                                    del form_vistoria.cleaned_data["alocacao"]
                                alocacao_concluida = True
                        else:
                            form_vistoria._errors["alocacao"] = form_vistoria.error_class([u'Não existem equipes com vagas disponíveis!'])
                            del form_vistoria.cleaned_data["alocacao"]
                            alocacao_concluida = True

                        if cont >= 1000:
                            dajax = process_modal(dajax, 'msg', u'Limite máximo de iterações atingido! Caso o erro persista, contate o suporte do sistema.', True)
                            dajax = process_form_vistoria(dajax)
                            form_vistoria._errors["alocacao_2_turno"] = form_vistoria.error_class([u'Limite máximo de iterações atingido! Caso o erro persista, contate o suporte do sistema.'])
                            del form_vistoria.cleaned_data["alocacao_2_turno"]
                            alocacao_concluida = True


                    if form_vistoria.is_valid():
                        # dajax = message_status(dajax, 'success', u"Vistoria efetuada com sucesso!", True)
                        dajax = process_modal(dajax, 'msg', u'<p style="text-align: center;">Vistoria efetuada com sucesso!<br><br><a href="%s" class="btn btn-default" target="_blank"><span class="glyphicon glyphicon-print"></span> Imprimir comprovante</a></p>' % reverse('report-veiculos:veiculo-alocado', args=(veiculo_alocado.pk,)), True)
                        dajax = process_form_vistoria(dajax)

                        return dajax.json()

                dajax = process_form_vistoria(dajax, veiculo=veiculo, exibe=True, request=request,
                                              form_vistoria=form_vistoria, form_motorista=form_pessoa_motorista, segundo_turno=turno)
            else:
            # Caso contrário, exibe mensagem de erro
                dajax = process_modal(dajax, 'msg', u"Ocorreu um erro no envio do modal", True)

        except Exception, e:
            dajax = process_modal(dajax, 'msg',
                                  "Ocorreu um erro: <strong>%s</strong><br>Favor entrar em contato com o departamento de TI." % e,
                                  True)
    else:
        dajax = process_modal(dajax, 'msg', u"Instrução inválida!", True)
    return dajax.json()

@dajaxice_register()
def desalocar_veiculo(request, id_veiculo, exibe_vistoria=False, turno=None, timeout=False):
    dajax = Dajax()

    if request.is_ajax():
        try:
            if turno and datetime.date.today() > request.eleicao_atual.data_turno_2 or not turno and datetime.date.today() > request.eleicao_atual.data_turno_1:
                dajax = process_modal(dajax, 'msg',
                                      u"Não é possivel desalocar esse veículo, o turno referente a essa alocação já passou.",
                                      True)
            else:
                veiculo_alocado = get_object_or_404(VeiculoAlocado, pk=int(id_veiculo))
                veiculo = veiculo_alocado.veiculo
                placa = veiculo.placa
                veiculo_alocado.delete()

                if exibe_vistoria:
                    motorista = veiculo.motorista_veiculo.filter(segundo_turno=turno).first()
                    motorista.veiculo = None
                    motorista.save()
                    form_motorista = MotoristaVistoriaForm(initial={'motorista': motorista.pessoa, 'id': motorista.pessoa.id},
                                                           instance=motorista.pessoa)
                    dajax = process_form_vistoria(dajax=dajax, veiculo=veiculo, exibe=True, request=request,
                                                  form_motorista=form_motorista, segundo_turno=turno)

                dajax.script("$.notify({theme:'sucesso', title:'Veiculo da placa %s desalocado com sucesso!'});" % placa.upper())
                if timeout:
                    dajax.script("window.setTimeout('location.reload()', 3000);")
        except Exception, e:
            dajax = process_modal(dajax, 'msg',
                                  "Ocorreu um erro: <strong>%s</strong><br>Favor entrar em contato com o departamento de TI." % e,
                                  True)
    return dajax.json()


@dajaxice_register()
def recarregar_monitoramento(request, turno):
    """
    Atualiza o select dos modelos de acordo com a marca selecionada
    """
    dajax = Dajax()
    if request.is_ajax():
        try:
            monitoramento = monta_monitoramento(request, turno)
            render = render_to_string('veiculos/vistoria/monitor-detalhe.html', RequestContext(request, {'equipes_monitoracao': monitoramento}))
            dajax.assign('#monitor-detalhe', 'innerHTML', render)
        except Exception, e:
            dajax = process_modal(dajax, 'msg',
                                  "Ocorreu um erro: <strong>%s</strong><br>Favor entrar em contato com o departamento de TI." % e,
                                  True)
    else:
        dajax = process_modal(dajax, 'msg', u"Instrução inválida!", True)
    return dajax.json()


def equipes_c_vagas_locais(equipe):
    return ((equipe.estimativa_local or 0) - equipe.veiculos_alocados_local) > 0


def locais_c_vagas(local):
    soma_estimativa = local.alocacao_set.aggregate(models.Sum('quantidade')).get('quantidade__sum')
    total_veiculos = local.veiculoalocado_set.count()
    return soma_estimativa - total_veiculos > 0


def alocacao_c_vagas(alocacao):
    total_veiculos = alocacao.local_votacao.veiculoalocado_set.filter(perfil=alocacao.perfil_veiculo, segundo_turno=alocacao.segundo_turno).count()
    return alocacao.quantidade - total_veiculos > 0