#-*- coding: utf-8 -*-
import csv
from core.models import Local
from django.shortcuts import render, redirect
from forms import EleicaoForm, LocalImportarForm
from models import Eleicao, LocalVotacao, Secao
from middleware import definir_eleicao_padrao

def ler_csv(request, f):
    linhas = list(csv.reader(f, delimiter=','))
    for linha in linhas[1:]:
        id_local, nome, endereco, bairro, secao, num_eleitores = linha
        try:
            local = Local.objects.get(pk=int(id_local))
            local.nome, local.endereco, local.bairro = nome, endereco, bairro
            local.save()
        except:
            local = Local.objects.create(id_local=int(id_local), nome=nome, endereco=endereco, bairro=bairro)
        try:
            local_votacao = LocalVotacao.objects.get(local=local, eleicao=request.eleicao_atual)
        except:
            local_votacao = LocalVotacao.objects.create(local=local, eleicao=request.eleicao_atual)
        try:
            secao = Secao.objects.get(num_secao=int(secao), eleicao=request.eleicao_atual)
            secao.local_votacao, secao.num_eleitores = local_votacao, num_eleitores
            secao.save()
        except:
            secao = Secao.objects.create(num_secao=int(secao), eleicao=request.eleicao_atual, local_votacao = local_votacao, num_eleitores=num_eleitores)

#Módulo de eleição

def eleicao_cadastrar(request):
    titulo = u'Cadastrar Eleição'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EleicaoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            definir_eleicao_padrao(request)
            return redirect('eleicao:index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EleicaoForm()
    return render(request, 'eleicao/eleicao/form.html', locals())

def eleicao_editar(request, id_eleicao):
    titulo = u'Editar Eleição'
    eleicao = Eleicao.objects.get(pk=int(id_eleicao))
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EleicaoForm(request.POST, instance=eleicao)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            
            return redirect('eleicao:index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EleicaoForm(instance=eleicao)
    return render(request, 'eleicao/eleicao/form.html', locals())


def eleicao_index(request):
    titulo = u'Eleições'
    eleicoes = Eleicao.objects.all().order_by('-atual','data_turno_1', 'data_turno_2')
    return render(request, 'eleicao/eleicao/index.html', locals())


#Módulo de locais

def local_importar(request):
    titulo = u'Importar Locais de Votação'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LocalImportarForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            ler_csv(request, request.FILES['arquivo'])
            return redirect('local:index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LocalImportarForm()
    return render(request, 'eleicao/local_votacao/importar.html', locals())


def local_index(request):
    locais = LocalVotacao.objects.filter(eleicao=request.eleicao_atual).order_by('local__nome')
    return render(request, 'eleicao/local_votacao/index.html', locals())