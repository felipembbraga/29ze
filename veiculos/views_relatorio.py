#-*- coding: utf-8 -*-
'''
Created on 07/08/2014

@author: felipe
'''
import datetime
from datetime import date
from django.forms.models import modelform_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context
from excel_response import ExcelResponse
from veiculos.forms import FrequenciaForm, RelatorioDiaForm
import webodt
from webodt.converters import converter
from eleicao.models import Equipe
from models import Veiculo, VeiculoSelecionado
from acesso.models import OrgaoPublico
from veiculos.models import VeiculoAlocado, PerfilVeiculo


@permission_required('veiculos.view_veiculo', raise_exception=True)
@login_required(login_url='acesso:login-veiculos')
def relatorio_veiculos(request):
    if isinstance(request.user, OrgaoPublico):
        veiculos = Veiculo.objects.filter(orgao= request.user, eleicao = request.eleicao_atual).order_by('marca__nome', 'modelo__nome')
    else:
        veiculos = Veiculo.objects.all().order_by('marca__nome', 'modelo__nome')
    return render(request, 'veiculos/report/veiculos.html', locals())

def relatorio_admin_orgao_sem_veiculo(request):
    orgaos = OrgaoPublico.objects.all()
    lista_orgaos = []
    for orgao in orgaos:
        if orgao.veiculo_orgao.count() == 0:
            lista_orgaos.append(orgao)
    return render(request, 'veiculos/report/orgaos-sem-veiculos.html', locals())

def relatorio_veiculos_requisitados(request, id_orgao=None):
    if id_orgao:
        orgao = OrgaoPublico.objects.get(pk=int(id_orgao))
        veiculos = VeiculoSelecionado.objects.filter(veiculo__eleicao = request.eleicao_atual, veiculo__orgao=orgao).order_by('veiculo__orgao__nome_secretaria', 'veiculo__marca__nome', 'veiculo__modelo__nome')
    
    orgaos = OrgaoPublico.objects.all().order_by('nome_secretaria')
    Form = modelform_factory(
                Veiculo,
                fields=('orgao',),
                labels={'orgao':u'Selecionar Órgão: '})
    Form.base_fields['orgao'].queryset = orgaos
    form = Form({'orgao':id_orgao})
    form.fields['orgao'].widget.attrs.update({'class':'form-control'})
    return render(request, 'veiculos/report/veiculos_requisitados.html', locals())

def relatorio_veiculo_alocado(request, id_veiculo):
    veiculo = get_object_or_404(VeiculoAlocado, pk=int(id_veiculo))
    motorista = veiculo.veiculo.motorista_veiculo.first()
    data = datetime.datetime.now()
    def cronograma_local(c):
        if not c.local:
            c.local = veiculo.local_votacao.local
        c.local.endereco = c.local.endereco.upper()
        c.local.bairro = c.local.bairro.upper()
        if c.dia_montagem:
            if veiculo.local_votacao.local_montagem.turno=='v':
                c.dt_apresentacao = datetime.datetime(c.dt_apresentacao.year, c.dt_apresentacao.month,c.dt_apresentacao.day, 13,0)
            else:
                c.dt_apresentacao = datetime.datetime(c.dt_apresentacao.year, c.dt_apresentacao.month,c.dt_apresentacao.day, 7,0)
        return c
    cronogramas = map(cronograma_local, veiculo.perfil.cronograma_perfil.filter(eleicao = request.eleicao_atual).order_by('dt_apresentacao'))
    telefones = '/'.join(unicode(telefone) for telefone in motorista.pessoa.telefones_set.all()) if motorista else ''

    context = dict(
        veiculo='%s'%unicode(veiculo),
        motorista=motorista.pessoa.nome if motorista else 'SEM MOTORISTA',
        placa = veiculo.veiculo.placa,
        equipe = veiculo.equipe.nome,
        orgao=veiculo.veiculo.orgao.nome_secretaria,
        sigla = veiculo.equipe.sigla,
        cronogramas=cronogramas,
        perfil=veiculo.perfil.nome,
        telefones = telefones,
        endereco = motorista.pessoa.endereco if motorista else '',
        data=data
    )
    template = webodt.ODFTemplate('modelo_notificacao.odt')
    document = template.render(Context(context))
    conv = converter()
    pdf = conv.convert(document, format='pdf')
    return HttpResponse(pdf, mimetype='application/pdf')


def relatorio_veiculos_alocados(request, id_equipe=None):

    if id_equipe:
        equipe = get_object_or_404(Equipe, pk=int(id_equipe))
    equipes = Equipe.objects.filter(eleicao=request.eleicao_atual).order_by('nome')
    Form = modelform_factory(
                VeiculoAlocado,
                fields=('equipe',),
                labels={'equipe':u'Selecionar Equipe: '})
    Form.base_fields['equipe'].queryset = equipes
    form = Form({'equipe':id_equipe})
    form.fields['equipe'].widget.attrs.update({'class':'form-control'})
    return render(request, 'veiculos/report/veiculos_alocados.html', locals())

def relatorio_veiculos_alocados_por_perfil(request, id_perfil=None):

    if id_perfil:
        perfil = get_object_or_404(PerfilVeiculo, pk=int(id_perfil))
        equipes = perfil.equipes.filter(eleicao = request.eleicao_atual).exclude(veiculoalocado=None).order_by('nome')
        veiculos = perfil.veiculoalocado_set.filter(veiculo__eleicao = request.eleicao_atual).order_by('veiculo__motorista_veiculo__pessoa__nome')
    perfis = PerfilVeiculo.objects.all().order_by('nome')
    Form = modelform_factory(
                VeiculoAlocado,
                fields=('perfil',),
                labels={u'perfil':u'Selecionar Função: '})
    Form.base_fields['perfil'].queryset = perfis
    form = Form({'perfil':id_perfil})
    form.fields['perfil'].widget.attrs.update({'class':'form-control'})
    return render(request, 'veiculos/report/veiculos_alocados_perfil.html', locals())

@login_required
@permission_required('veiculos.monitor_vistoria', raise_exception=True)
def frequencia_motoristas(request):
    if request.POST:
        formulario = FrequenciaForm(request.POST)
        dict_equipe = None
        data = None
        if formulario.is_valid():
            data = formulario.cleaned_data['data_frequencia']
            equipe = formulario.cleaned_data['equipe']
            equipe = Equipe.objects.filter(veiculoalocado__perfil__cronograma_perfil__dt_apresentacao__range=(data, data.replace(day=data.day+1)), id=equipe.id).select_related()

            if equipe:
                equipe = equipe.first()
                veiculos_alocados = equipe.veiculoalocado_set.filter(perfil__cronograma_perfil__dt_apresentacao__range=(data, data.replace(day=data.day+1)))
                dict_equipe = {
                    'equipe': equipe,
                    'veiculos_equipe': veiculos_alocados.get_perfis_equipe(),
                    'locais': []
                }

                for local in equipe.local_equipe.all().order_by('local__nome'):
                    veiculos_alocados_local = veiculos_alocados.get_perfis_local().filter(local_votacao=local).order_by('veiculo__motorista_veiculo__pessoa__nome')

                    if veiculos_alocados_local:
                        dict_equipe['locais'].append({'local': local,
                                                      'veiculos_local': veiculos_alocados_local})
        return render(request, 'veiculos/report/frequencia_motoristas.html', {'dict_equipe': dict_equipe, 'form': formulario, 'data': data})

    formulario = FrequenciaForm()
    return render(request, 'veiculos/report/frequencia_motoristas.html', {'form': formulario})


@permission_required('eleicao.view_local_votacao', raise_exception=True)
def relatorio_motoristas_dia(request):
    formulario = RelatorioDiaForm()

    if request.POST:
        formulario = RelatorioDiaForm(request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data['data_frequencia']
            veiculos = VeiculoAlocado.objects.filter(perfil__cronograma_perfil__dt_apresentacao__range=(data, data.replace(day=data.day+1)))
            cabecalho = ['equipe', 'local', 'perfil', 'placa_veiculo', 'titulo_eleitor', 'nome_motorista', 'telefone_celular', 'telefone_residencial', ]
            data = [cabecalho,]
            for veiculoalocado in veiculos:
                data.append([veiculoalocado.equipe,
                             veiculoalocado.local_votacao,
                             veiculoalocado.perfil,
                             veiculoalocado.veiculo.placa,
                             veiculoalocado.veiculo.motorista_veiculo.first().pessoa.titulo_eleitoral,
                             veiculoalocado.veiculo.motorista_veiculo.first().pessoa.nome,
                             veiculoalocado.veiculo.motorista_veiculo.first().pessoa.tel_celular(),
                             veiculoalocado.veiculo.motorista_veiculo.first().pessoa.tel_residencial(),])

            return ExcelResponse(data, 'motoristas_do_dia')
    return render(request, 'veiculos/report/frequencia_motoristas.html', {'form': formulario})
