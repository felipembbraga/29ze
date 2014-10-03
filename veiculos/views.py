#-*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query_utils import Q
from django.forms.models import modelform_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from acesso.decorators import orgao_atualizar
from acesso.models import OrgaoPublico
from core.models import Modelo
from django.template.context import RequestContext
from eleicao.models import LocalVotacao, Equipe, EquipesAlocacao
from filters import VeiculoFilter
from forms import VeiculoForm, MotoristaForm
from models import Veiculo, VeiculoSelecionado
from utils.forms import NumPorPaginaForm
from utils.Response import NotifyResponse
from veiculos.filters import VeiculoAlocadoFilter
from veiculos.forms import PerfilVeiculoForm, CronogramaForm, AlocacaoForm
from veiculos.models import PerfilVeiculo, CronogramaVeiculo, Alocacao, VeiculoAlocado
import datetime


@orgao_atualizar
@login_required(login_url='acesso:login-veiculos')
def index(request):
    return render(request, 'veiculos/index.html')


@orgao_atualizar
@login_required(login_url='acesso:login-veiculos')
def info(request):
    return render(request, 'veiculos/info.html')


@orgao_atualizar
@permission_required('veiculos.add_veiculo', raise_exception=True)
@login_required(login_url='acesso:login-veiculos')
def veiculo_cadastrar(request):
    if request.method == 'POST':
        if request.POST.get('marca') != '':
            VeiculoForm.base_fields['modelo'].choices = [('','---------')] + list(Modelo.objects.filter(marca__pk=int(request.POST.get('marca'))).order_by('nome').values_list('pk', 'nome'))
        else:
            VeiculoForm.base_fields['modelo'].choices = [('','---------')]
        v = Veiculo(orgao = request.user, eleicao=request.eleicao_atual)
        form = VeiculoForm(request.POST, instance = v)
        form_motorista = MotoristaForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('cadastrar_motorista'):
                if form_motorista.is_valid():
                    veiculo = form.save(commit=False)
                    veiculo.motorista_titulo_eleitoral = form_motorista.cleaned_data['motorista_titulo_eleitoral']
                    veiculo.motorista_nome = form_motorista.cleaned_data['motorista_nome']
                    veiculo.endereco = form_motorista.cleaned_data['endereco']
                    veiculo.tel_residencial = form_motorista.cleaned_data['tel_residencial']
                    veiculo.tel_celular = form_motorista.cleaned_data['tel_celular']
                    veiculo.save()
                    messages.success(request, u'Veículo cadastrado com sucesso')
                    return redirect('veiculo:index')
            else:
                form.save()
                messages.success(request, u'Veículo cadastrado com sucesso')
                return redirect('veiculo:index')
    else:
        VeiculoForm.base_fields['modelo'].choices = [('','---------')]
        form = VeiculoForm()
        form_motorista = MotoristaForm()
    return render(request,'veiculos/veiculo/form.html', locals())


@orgao_atualizar
@permission_required('veiculos.change_veiculo', raise_exception=True)
@login_required(login_url='acesso:login-veiculos')
def veiculo_editar(request, id_veiculo):
    veiculo = get_object_or_404(Veiculo, pk=int(id_veiculo))
    VeiculoForm.base_fields['modelo'].choices = [('','---------')] + list(Modelo.objects.filter(marca=veiculo.marca).order_by('nome').values_list('pk', 'nome'))
    if request.method == 'POST':
        if request.POST.get('marca') != '':
            VeiculoForm.base_fields['modelo'].choices = [('','---------')] + list(Modelo.objects.filter(marca__pk=int(request.POST.get('marca'))).order_by('nome').values_list('pk', 'nome'))
        else:
            VeiculoForm.base_fields['modelo'].choices = [('','---------')]
        form = VeiculoForm(request.POST, instance = veiculo)
        form_motorista = MotoristaForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('cadastrar_motorista'):
                if form_motorista.is_valid():
                    v = form.save(commit=False)
                    v.motorista_titulo_eleitoral = form_motorista.cleaned_data['motorista_titulo_eleitoral']
                    v.motorista_nome = form_motorista.cleaned_data['motorista_nome']
                    v.endereco = form_motorista.cleaned_data['endereco']
                    v.tel_residencial = form_motorista.cleaned_data['tel_residencial']
                    v.tel_celular = form_motorista.cleaned_data['tel_celular']
                    v.save()
                    messages.success(request, u'Veículo editado com sucesso')
                    return redirect('veiculo:index')
            else:
                v = form.save(commit=False)
                v.motorista_titulo_eleitoral = None
                v.motorista_nome = None
                v.endereco = None
                v.tel_residencial = None
                v.tel_celular = None
                v.save()
                messages.success(request, u'Veículo editado com sucesso')
                return redirect('veiculo:index')
    else:
        if veiculo.motorista_titulo_eleitoral:
            
            VeiculoForm.base_fields['cadastrar_motorista'].initial=True
        form = VeiculoForm(instance=veiculo)
        form_motorista = MotoristaForm(instance=veiculo)
    return render(request,'veiculos/veiculo/form.html', locals())


@orgao_atualizar
@permission_required('veiculos.view_veiculo', raise_exception=True)
@login_required(login_url='acesso:login-veiculos')
def veiculo_index(request):
    if isinstance(request.user, OrgaoPublico):
        veiculos = Veiculo.objects.filter(orgao= request.user, eleicao = request.eleicao_atual).order_by('marca__nome', 'modelo__nome')
    else:
        veiculos = Veiculo.objects.all()
    return render(request, 'veiculos/veiculo/index.html', locals())


def veiculo_ajax_get_modelo(request, id_marca):
    modelos = Modelo.objects.filter(marca__pk=int(id_marca)).order_by('nome')
    json = serializers.serialize('json', modelos)
    return HttpResponse(json, mimetype="application/json")


@orgao_atualizar
@permission_required('veiculos.delete_veiculo', raise_exception=True)
@login_required(login_url='acesso:login-veiculos')
def veiculo_excluir(request, id_veiculo):
    if request.is_ajax():
        raise PermissionDenied
    veiculo = get_object_or_404(Veiculo, pk=int(id_veiculo))
    if request.method == 'POST':
        if request.POST.get('excluir-confirmar'):
            try:
                veiculo = Veiculo.objects.get(pk=int(id_veiculo))
                veiculo.delete()
                messages.success(request, u'Veículo excluido com sucesso')
                return redirect('veiculo:index')
            except:
                messages.error(request, u'Erro ao deletar o veículo')
        messages.error(request, u'Comando errado')
    return render(request, 'veiculos/veiculo/excluir.html', locals())


@login_required
def veiculo_listar(request, id_orgao=None):
    if id_orgao:
        orgao = OrgaoPublico.objects.get(pk=int(id_orgao))
        queryset = Veiculo.objects.filter(eleicao = request.eleicao_atual, orgao=orgao)
        
    else:
        queryset = Veiculo.objects.filter(eleicao = request.eleicao_atual)
    total_requisitados = queryset.exclude(veiculo_selecionado=None).count()
    lista_veiculos = queryset.exclude(estado=3).order_by('orgao__nome_secretaria', 'marca__nome', 'modelo__nome')
    
    filtro = VeiculoFilter(request.GET, queryset = lista_veiculos)
    total_com_motorista = filtro.qs.exclude(motorista_titulo_eleitoral=None).count()
    total_sem_motorista = filtro.qs.filter(motorista_titulo_eleitoral=None).count()
    
    form_pagina = NumPorPaginaForm(request.GET)
    num_por_pagina = form_pagina.is_valid() and int(form_pagina.cleaned_data['num_por_pagina']) or 10
    paginator = Paginator(filtro.qs, num_por_pagina)
    pagina = request.GET.get('pagina')
    try:
        veiculos = paginator.page(pagina)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        veiculos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        veiculos = paginator.page(paginator.num_pages)
    orgaos = OrgaoPublico.objects.all().order_by('nome_secretaria')
    form = modelform_factory(
                Veiculo,
                fields=('orgao',),
                labels={'orgao':u'Selecionar Órgão: '})
    form.base_fields['orgao'].queryset = orgaos
    form = form({'orgao':id_orgao})
    form.fields['orgao'].widget.attrs.update({'class':'form-control'})
    return render(request, 'veiculos/veiculo/listar.html', locals())


@login_required
def veiculo_requisitar(request, id_veiculo):
    if not request.is_ajax():
        raise PermissionDenied
    veiculo = get_object_or_404(Veiculo, pk=int(id_veiculo))
    VeiculoSelecionado.objects.get_or_create(veiculo=veiculo)
    return NotifyResponse('Sucesso', theme='sucesso')


@login_required
def veiculo_liberar(request, id_veiculo):
    if not request.is_ajax():
        raise PermissionDenied
    veiculo = get_object_or_404(Veiculo, pk=int(id_veiculo))
    if hasattr(veiculo, 'veiculo_selecionado'):
        veiculo.veiculo_selecionado.delete()
    return NotifyResponse('Sucesso', theme='sucesso')


@login_required
def veiculo_detalhar(request, id_veiculo):
    titulo = 'Detalhar veículo'
    veiculo = get_object_or_404(Veiculo, pk=int(id_veiculo))
    motorista = veiculo.motorista_veiculo.filter(eleicao=veiculo.eleicao).first()
    return render(request, 'veiculos/veiculo/detalhar.html', locals())

def perfil_veiculo_cadastrar(request):
    titulo = u'Cadastrar Perfil de Veículo'
    if request.method == 'POST':
        form = PerfilVeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('perfil-veiculo:detalhar', form.instance.pk)
    else:
        form = PerfilVeiculoForm()
    return render(request, 'veiculos/perfil_veiculo/form.html', locals())


def perfil_veiculo_listar(request):
    titulo = u'Perfís de Veículo'
    pesquisar = request.GET.get('pesquisar') and request.GET.get('pesquisar') or ''
    if pesquisar != '':
        lista_perfis = PerfilVeiculo.objects.filter(nome__icontains=pesquisar)
    else:
        lista_perfis = PerfilVeiculo.objects.all().order_by('nome')
    paginator = Paginator(lista_perfis, 15)
    pagina = request.GET.get('pagina')
    try:
        perfis = paginator.page(pagina)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        perfis = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        perfis = paginator.page(paginator.num_pages)
    return render(request, 'veiculos/perfil_veiculo/listar.html', locals())


def perfil_veiculo_editar(request, id_perfil):
    titulo = u'Editar Perfil de Veículo'
    perfil = get_object_or_404(PerfilVeiculo, pk=int(id_perfil))
    if request.method == 'POST':
        form = PerfilVeiculoForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil-veiculo:detalhar', form.instance.pk)
    else:
        form = PerfilVeiculoForm(instance=perfil)
    return render(request, 'veiculos/perfil_veiculo/form.html', locals())


def perfil_veiculo_detalhar(request, id_perfil):
    """
    :param request:
    :param id_perfil:
    :return:
    """
    perfil = get_object_or_404(PerfilVeiculo, pk=int(id_perfil))
    cronogramas = perfil.cronograma_perfil.filter(eleicao = request.eleicao_atual).order_by('dt_apresentacao')
    titulo = u'Detalhar Perfil de Veículo'
    return render(request, 'veiculos/perfil_veiculo/detalhar.html', locals())


def cronograma_cadastrar(request, id_perfil):
    """
    :param request:
    :param id_perfil:
    :return:
    """
    titulo = u'Cadastrar Cronograma de Veículo'
    perfil = get_object_or_404(PerfilVeiculo, pk=int(id_perfil))
    cronograma = CronogramaVeiculo(perfil=perfil, eleicao=request.eleicao_atual)
    if request.method == 'POST':
        form = CronogramaForm(request.POST, instance=cronograma)
        if form.is_valid():
            cronograma.local = form.cleaned_data['local']
            parametros_datetime = [form.cleaned_data['data'].year, form.cleaned_data['data'].month, form.cleaned_data['data'].day, form.cleaned_data['hora'].hour, form.cleaned_data['hora'].minute]
            cronograma.dt_apresentacao = datetime.datetime(*parametros_datetime)
            cronograma.save()
            return redirect('perfil-veiculo:detalhar', perfil.pk)
    else:
        form = CronogramaForm(instance=cronograma)
    return render(request, 'veiculos/cronograma_veiculo/form.html', locals())


def cronograma_editar(request, id_cronograma):
    """
    :param request:
    :param id_perfil:
    :return:
    """
    titulo = u'Editar Cronograma de Veículo'
    cronograma = get_object_or_404(CronogramaVeiculo, pk=int(id_cronograma))
    perfil = cronograma.perfil
    if request.method == 'POST':
        form = CronogramaForm(request.POST, instance=cronograma)
        if form.is_valid():
            cronograma.local = form.cleaned_data['local']
            parametros_datetime = [form.cleaned_data['data'].year, form.cleaned_data['data'].month, form.cleaned_data['data'].day, form.cleaned_data['hora'].hour, form.cleaned_data['hora'].minute]
            cronograma.dt_apresentacao = datetime.datetime(*parametros_datetime)
            cronograma.save()
            return redirect('perfil-veiculo:detalhar', perfil.pk)
    else:
        form = CronogramaForm(instance=cronograma)
    return render(request, 'veiculos/cronograma_veiculo/form.html', locals())


def cronograma_excluir(request, id_cronograma):
    cronograma = get_object_or_404(CronogramaVeiculo, pk=int(id_cronograma))
    perfil = cronograma.perfil
    try:
        cronograma.delete()
        messages.success(request, u'Cronograma removido com sucesso')
        return redirect('perfil-veiculo:detalhar', perfil.pk)
    except:
        messages.error(request, u'Erro ao remover o cronograma')
        return redirect('perfil-veiculo:detalhar', perfil.pk)

def alocacao_editar(request, id_equipe, id_perfil, id_local=None):
    total_veiculos = Veiculo.objects.filter(eleicao = request.eleicao_atual).exclude(veiculo_selecionado=None).count()
    equipes = Equipe.objects.filter(eleicao=request.eleicao_atual)
    veiculos_alocados = 0
    for e in equipes:
        veiculos_alocados += e.total_veiculos_estimados()

    equipe = get_object_or_404(Equipe, pk = int(id_equipe))
    perfil_veiculo = get_object_or_404(PerfilVeiculo, pk = int(id_perfil))
    local = id_local and get_object_or_404(LocalVotacao, pk=int(id_local)) or None
    alocacao = get_object_or_404(Alocacao, perfil_veiculo = perfil_veiculo, equipe=equipe, local_votacao=local)
    if request.method=='POST':
        form = AlocacaoForm(request.POST, instance=alocacao, eleicao = request.eleicao_atual)
        if form.is_valid():
            form.save()
            return redirect('equipe:detalhar-estimativa', equipe.pk)
    else:
        form = AlocacaoForm(instance=alocacao, eleicao = request.eleicao_atual)
    return render(request, 'veiculos/alocacao/form.html', locals())


@login_required
@permission_required('veiculos.inspection_veiculo', raise_exception=True)
def index_vistoria(request):
    return render(request, 'veiculos/vistoria/index.html')


@login_required
@permission_required('veiculos.inspection_veiculo', raise_exception=True)
def veiculo_vistoria(request):
    return render(request, 'veiculos/vistoria/cadastrar.html')


@login_required
@permission_required('veiculos.inspection_veiculo', raise_exception=True)
def veiculo_vistoria_listagem(request, id_equipe=None):

    if id_equipe:
        equipe = Equipe.objects.get(pk=int(id_equipe))
        queryset = VeiculoAlocado.objects.filter(veiculo__eleicao = request.eleicao_atual, equipe=equipe)

    else:
        queryset = VeiculoAlocado.objects.filter(veiculo__eleicao = request.eleicao_atual)
    total_veiculos = queryset.count()
    lista_veiculos = queryset.order_by('equipe__nome', 'veiculo__marca__nome', 'veiculo__modelo__nome')
    pesquisar = request.GET.get('pesquisar') and request.GET.get('pesquisar') or ''
    if pesquisar != '':
       lista_veiculos = lista_veiculos.filter(Q(veiculo__motorista_veiculo__pessoa__nome__icontains=pesquisar)| Q(veiculo__placa__icontains=pesquisar))

    #filtro = VeiculoAlocadoFilter(request.GET, queryset = lista_veiculos)
    #total_com_motorista = filtro.qs.exclude(motorista_titulo_eleitoral=None).count()
    #total_sem_motorista = filtro.qs.filter(motorista_titulo_eleitoral=None).count()

    form_pagina = NumPorPaginaForm(request.GET)
    num_por_pagina = form_pagina.is_valid() and int(form_pagina.cleaned_data['num_por_pagina']) or 10
    paginator = Paginator(lista_veiculos, num_por_pagina)
    pagina = request.GET.get('pagina')
    try:
        veiculos = paginator.page(pagina)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        veiculos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        veiculos = paginator.page(paginator.num_pages)
    equipes = Equipe.objects.filter(eleicao=request.eleicao_atual).exclude(veiculoalocado=None).order_by('nome')
    formequipe = modelform_factory(
                VeiculoAlocado,
                fields=('equipe',),
                labels={'equipe':u'Selecionar uma equipe: '})
    formequipe.base_fields['equipe'].queryset = equipes
    if id_equipe:
        form = formequipe({'equipe':id_equipe})
    else:
        form = formequipe()
    form.fields['equipe'].widget.attrs.update({'class':'form-control'})
    return render(request, 'veiculos/vistoria/listar.html', locals())


@login_required
@permission_required('veiculos.monitor_vistoria', raise_exception=True)
def monitorar_vistoria(request):
    return render(request, 'veiculos/vistoria/monitor.html', RequestContext(request, {'equipes_monitoracao': monta_monitoramento(request)}))


def monta_monitoramento(request):
    equipes = EquipesAlocacao.objects.filter(eleicao=request.eleicao_atual).order_by('equipe__nome')
    equipe_monitoracao = []
    for equipe in equipes:
        dict = {'equipe': equipe.equipe,
                'total_estimado': equipe.total_estimativa,
                'estimado': equipe.total_estimativa - equipe.veiculos_alocados,
                'alocado': equipe.veiculos_alocados,
                'percentual_alocado': (100 * equipe.veiculos_alocados) / equipe.total_estimativa}

        dict['percentual_estimado'] = 100 - dict['percentual_alocado']

        equipe_monitoracao.append(dict)

    return equipe_monitoracao