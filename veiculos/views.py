#-*- coding: utf-8 -*-

from core.models import Modelo
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from forms import VeiculoForm, MotoristaForm
from models import Veiculo
from acesso.models import OrgaoPublico
from django.core.exceptions import PermissionDenied
# Create your views here.


@login_required(login_url='acesso:login-veiculos')
def index(request):
    return render(request, 'veiculos/index.html')

@login_required(login_url='acesso:login-veiculos')
def info(request):
    return render(request, 'veiculos/info.html')

@permission_required('veiculos.add_veiculo', raise_exception=True)
@login_required(login_url='acesso:login-veiculos')
def veiculo_cadastrar(request):
    if request.method == 'POST':
        if request.POST.get('marca') != '':
            VeiculoForm.base_fields['modelo'].choices = [('','---------')] + list(Modelo.objects.filter(marca__pk=int(request.POST.get('marca'))).values_list('pk', 'nome'))
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

@permission_required('veiculos.change_veiculo', raise_exception=True)
@login_required(login_url='acesso:login-veiculos')
def veiculo_editar(request, id_veiculo):
    veiculo = get_object_or_404(Veiculo, pk=int(id_veiculo))
    VeiculoForm.base_fields['modelo'].choices = [('','---------')] + list(Modelo.objects.filter(marca=veiculo.marca).values_list('pk', 'nome'))
    if request.method == 'POST':
        if request.POST.get('marca') != '':
            VeiculoForm.base_fields['modelo'].choices = [('','---------')] + list(Modelo.objects.filter(marca__pk=int(request.POST.get('marca'))).values_list('pk', 'nome'))
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

@permission_required('veiculos.view_veiculo', raise_exception=True)
@login_required(login_url='acesso:login-veiculos')
def veiculo_index(request):
    if isinstance(request.user, OrgaoPublico):
        veiculos = Veiculo.objects.filter(orgao= request.user, eleicao = request.eleicao_atual).order_by('marca__nome', 'modelo__nome')
    else:
        veiculos = Veiculo.objects.all()
    return render(request, 'veiculos/veiculo/index.html', locals())

def veiculo_ajax_get_modelo(request, id_marca):
    modelos = Modelo.objects.filter(marca__pk=int(id_marca))
    json = serializers.serialize('json', modelos)
    return HttpResponse(json, mimetype="application/json")

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