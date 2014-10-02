# -*- coding: utf-8 -*-
from core.models import Modelo, Pessoa
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.template.loader import render_to_string
from eleicao.models import Equipe, EquipesAlocacao
from models import Veiculo, Motorista
from veiculos.forms import VeiculoVistoriaForm, VistoriaForm, MotoristaVistoriaForm
from veiculos.models import VeiculoSelecionado, VeiculoAlocado
from django.db import models


@dajaxice_register()
def consultar_veiculo(request, placa):
    """
    Consulta um veículo para efetuar a vistoria
    - Caso não esteja cadastrado, o sistema dará a possibilidade de cadastro do veículo
    - Caso o veículo não tenha sido solicitado, pergunta se o servidor deseja solicitar o mesmo
    """
    dajax = Dajax()
    modal = None
    msg = ''

    if request.is_ajax():
        try:
            if Veiculo.objects.filter(placa__iexact=placa, veiculo_selecionado__isnull=False).exists():
            # Caso o veículo exista no sistema
                veiculo = Veiculo.objects.get(placa__iexact=placa, veiculo_selecionado__isnull=False)
                if hasattr(veiculo, 'veiculoalocado') and veiculo.veiculoalocado is not None:
                    dajax = message_status(dajax, 'success', u"Veículo encontrado! O mesmo já foi alocado.", True)
                    veiculo_alocado = veiculo.veiculoalocado
                    if veiculo_alocado.local_votacao:
                        form_vistoria = VistoriaForm()
                    else:
                        form_vistoria = VistoriaForm(initial={'alocacao': 1, 'equipe': veiculo_alocado.equipe,
                                                              'perfil': veiculo_alocado.perfil})
                    form_motorista = MotoristaVistoriaForm(initial={'motorista': veiculo.motorista_veiculo.first(),
                                                                    'id': veiculo.motorista_veiculo.first().pessoa.id},
                                                           instance=veiculo.motorista_veiculo.first().pessoa)
                    dajax = process_form_vistoria(dajax, veiculo, True, request, form_vistoria, form_motorista)
                else:
                    dajax = message_status(dajax, 'success', u"Veículo encontrado!", True)
                    dajax = process_form_vistoria(dajax, veiculo, True, request)
            elif Veiculo.objects.filter(placa__iexact=placa, veiculo_selecionado__isnull=True).exists():
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
def cadastrar_veiculo(request, placa, formulario):
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
                    VeiculoSelecionado.objects.get_or_create(veiculo=veiculo)  # realiza a requisição do veículo automaticamente

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
def requisitar_veiculo(request, placa):
    """
    Requisita um veículo ainda não requisitado
    """
    dajax = Dajax()
    veiculo = Veiculo.objects.filter(placa__iexact=placa)

    if veiculo:
    # Caso exista veículo com a placa informada no sistema, requisita o mesmo
        VeiculoSelecionado.objects.get_or_create(veiculo=veiculo.first())
        message = "Veículo requisitado com sucesso!"
        status = 'success'

        dajax = process_form_vistoria(dajax, veiculo.first(), True, request)
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


def process_form_vistoria(dajax, veiculo=None, exibe=False, request=None, form_vistoria=None, form_motorista=None):
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
            form_motorista = MotoristaVistoriaForm(initial={'motorista': veiculo.motorista_veiculo.first(),
                                                            'id': veiculo.motorista_veiculo.first().pessoa.id},
                                                   instance=veiculo.motorista_veiculo.first().pessoa)
        else:
            form_motorista = MotoristaVistoriaForm()

        render = render_to_string('veiculos/vistoria/vistoria_form.html', RequestContext(request,
                                                                                         {'veiculo': veiculo,
                                                                                          'form_vistoria': form_vistoria,
                                                                                          'form_motorista': form_motorista}))
        dajax.assign('#cadastrar-vistoria .panel-body', 'innerHTML', render)
        dajax.script("$('#cadastrar-vistoria').show();")
    else:
        dajax.assign('#cadastrar-vistoria .panel-body', 'innerHTML', '')
        dajax.script("$('#cadastrar-vistoria').hide();")

    return dajax


@dajaxice_register()
def consulta_motorista(request, id_motorista):
    """
    Preenche os campos do motorista com os dados encontrados no BD
    """
    dajax = Dajax()
    if request.is_ajax():
        try:

            if id_motorista:
                motorista = Motorista.objects.get(pk=int(id_motorista))
                if motorista.veiculo:
                    dajax = process_modal(dajax, 'requisitar-motorista',
                                          u'Motorista vinculado a outro veículo, deseja vincular a este?',
                                          True, u'Motorista vinculado a veículo')
                elif True:
                    dajax = process_modal(dajax, 'msg',
                                          u'Não é possivel selecionar esse motorista. O mesmo se encontra vinculado a veículo já alocado.', True)
                    return dajax.json()

                dajax.assign('#id_id', 'value', motorista.pessoa.id)
                dajax.assign('#id_titulo_eleitoral', 'value', motorista.pessoa.titulo_eleitoral)
                dajax.assign('#id_nome', 'value', motorista.pessoa.nome)
                dajax.assign('#id_endereco', 'value', motorista.pessoa.endereco)

        except Exception, e:
            dajax = process_modal(dajax, 'msg',
                                  "Ocorreu um erro: <strong>%s</strong><br>Favor entrar em contato com o departamento de TI." % e,
                                  True)
    else:
        dajax = process_modal(dajax, 'msg', u"Instrução inválida!", True)
    return dajax.json()


@dajaxice_register()
def cadastrar_vistoria(request, formulario):
    """
    Efetua o cadastro da vistoria
    """
    dajax = Dajax()

    if request.is_ajax():
        try:
            if formulario:
                # Caso esteja sendo enviado o formulário
                formulario = deserialize_form(formulario)
                veiculo = Veiculo.objects.get(placa__iexact=formulario.get('placa_veiculo_vist'))
                if formulario.get('id'):
                    pessoa_motorista = Pessoa.objects.get(id=int(formulario.get('id')))
                    form_pessoa_motorista = MotoristaVistoriaForm(formulario, instance=pessoa_motorista)
                else:
                    form_pessoa_motorista = MotoristaVistoriaForm(formulario)
                form_vistoria = VistoriaForm(formulario)

                if form_pessoa_motorista.is_valid() and form_vistoria.is_valid():
                    # Se os formulários forem válidos
                    pessoa_motorista = form_pessoa_motorista.save()

                    if not formulario.get('motorista'):
                        motorista = Motorista.objects.create(pessoa=pessoa_motorista, veiculo=veiculo, eleicao=request.eleicao_atual)
                    else:
                        motorista = form_pessoa_motorista.cleaned_data['motorista']
                        motorista.pessoa = pessoa_motorista
                        motorista.veiculo = veiculo
                        motorista.eleicao = request.eleicao_atual
                        motorista.save()

                    if not motorista.veiculo:
                        motorista.veiculo = veiculo

                    if form_vistoria.cleaned_data.get('alocacao') == '0':
                        import random
                        if form_vistoria.cleaned_data.get('alocacao_manual'):
                            equipe_auto = form_vistoria.cleaned_data.get('equipe_manual')
                        else:
                            equipe_auto = random.choice(filter(equipes_c_vagas_locais, EquipesAlocacao.objects.all().order_by('equipe__nome')))
                        equipe_auto = equipe_auto.equipe
                        local_auto = random.choice(filter(locais_c_vagas, equipe_auto.local_equipe.all()))
                        alocacao = random.choice(filter(alocacao_c_vagas, local_auto.alocacao_set.all()))
                        perfil = alocacao.perfil_veiculo
                        equipe = alocacao.equipe
                        local_votacao = local_auto
                    else:
                        perfil = form_vistoria.cleaned_data.get('perfil')
                        equipe = form_vistoria.cleaned_data.get('equipe').equipe
                        local_votacao = None

                    if not VeiculoAlocado.objects.filter(veiculo=veiculo).exists():
                        veiculo_alocado = VeiculoAlocado.objects.create(veiculo=veiculo, perfil=perfil, equipe=equipe,
                                                                        local_votacao=local_votacao)
                    else:
                        veiculo_alocado = VeiculoAlocado.objects.get(veiculo=veiculo)
                        veiculo_alocado.perfil = perfil
                        veiculo_alocado.equipe = equipe
                        veiculo_alocado.local_votacao = local_votacao
                        veiculo_alocado.save()

                    # dajax = message_status(dajax, 'success', u"Vistoria efetuada com sucesso!", True)
                    dajax = process_modal(dajax, 'msg', u'<p style="text-align: center;">Vistoria efetuada com sucesso!<br><br><a href="%s" class="btn btn-default" target="_blank"><span class="glyphicon glyphicon-print"></span> Imprimir comprovante</a></p>' % reverse('report-veiculos:veiculo-alocado', args=(veiculo_alocado.pk,)), True)
                    dajax = process_form_vistoria(dajax)

                    return dajax.json()

                dajax = process_form_vistoria(dajax, veiculo=veiculo, exibe=True, request=request,
                                              form_vistoria=form_vistoria, form_motorista=form_pessoa_motorista)
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


def equipes_c_vagas_locais(equipe):
    return (equipe.estimativa_local or 0 - equipe.veiculos_alocados_local) > 0


def locais_c_vagas(local):
    soma_estimativa = local.alocacao_set.aggregate(models.Sum('quantidade')).get('quantidade__sum')
    total_veiculos = local.veiculoalocado_set.count()
    return soma_estimativa - total_veiculos > 0

def alocacao_c_vagas(alocacao):
    total_veiculos = alocacao.local_votacao.veiculoalocado_set.count()
    return alocacao.quantidade - total_veiculos > 0