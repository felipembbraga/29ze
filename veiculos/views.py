#-*- coding: utf-8 -*-

from core.models import Modelo
from django import forms
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import modelform_factory

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from forms import VeiculoForm, MotoristaForm
from models import Veiculo
from acesso.models import OrgaoPublico
from django.core.exceptions import PermissionDenied
from acesso.decorators import orgao_atualizar
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

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
        
    lista_veiculos = queryset.exclude(estado=3).order_by('orgao__nome_secretaria', 'marca__nome', 'modelo__nome')
    total_com_motorista = lista_veiculos.exclude(motorista_titulo_eleitoral=None).count()
    total_sem_motorista = lista_veiculos.filter(motorista_titulo_eleitoral=None).count()
    paginator = Paginator(lista_veiculos, 15)
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
    Form = modelform_factory(
                Veiculo,
                fields=('orgao',),
                labels={'orgao':u'Filtrar por Órgão: '})
    Form.base_fields['orgao'].queryset = orgaos
    form = Form({'orgao':id_orgao})
    return render(request, 'veiculos/veiculo/listar.html', locals())
