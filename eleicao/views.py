#-*- coding: utf-8 -*-
import csv
import json
from core.models import Local
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from forms import EleicaoForm, LocalImportarForm, SecaoAgregarForm
from models import Eleicao, LocalVotacao, Secao
from middleware import definir_eleicao_padrao
from utils.Response import NotifyResponse

def javascript(request, nome_arquivo):
    return render(request, 'js/'+nome_arquivo, content_type='text/javascript')

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
    titulo = u'Locais de Votação'
    pesquisar = request.GET.get('pesquisar') and request.GET.get('pesquisar') or ''
    args = dict({'eleicao':request.eleicao_atual}) 
    if pesquisar != '':
        try:
            lista_locais = LocalVotacao.objects.filter(Q(local__nome__icontains=pesquisar)|Q(secao__num_secao=int(pesquisar)),
                                                   eleicao=request.eleicao_atual).distinct('local__nome').order_by('local__nome')
        except ValueError:
            lista_locais = LocalVotacao.objects.filter(local__nome__icontains=pesquisar,
                                                   eleicao=request.eleicao_atual).distinct('local__nome').order_by('local__nome')
    else:
        lista_locais = LocalVotacao.objects.filter(**args).order_by('local__nome')
    paginator = Paginator(lista_locais, 15)
    pagina = request.GET.get('pagina')
    try:
        locais = paginator.page(pagina)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        locais = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        locais = paginator.page(paginator.num_pages)
    
    return render(request, 'eleicao/local_votacao/index.html', locals())

@ensure_csrf_cookie
def local_detalhar(request, id_local):
    titulo = u'Local'
    local = get_object_or_404(LocalVotacao, pk=int(id_local), eleicao=request.eleicao_atual)
    #raise Exception(form['pk_secao'])
    return render(request, 'eleicao/local_votacao/detalhar.html', locals())

def local_editar(request, id_local):
    pass

def secao_agregar(request):
    if not request.is_ajax():
        raise PermissionDenied
    try:
        form = request.formClass(request.POST)
        if form.is_valid():
            if len(form.cleaned_data['pk_secao']) < 2:
                raise Exception('Selecione pelo menos duas Seções')
            secoes = Secao.objects.filter(pk__in=form.cleaned_data['pk_secao']).order_by('-num_eleitores')
            secao_principal = secoes[0]
            for secao in secoes[1:]:
                if secao.secao_secoes_agregadas.count() > 0:
                    secoes_filhos = secao.secao_secoes_agregadas.all()
                    for secao_filho in secoes_filhos:
                        secao_principal.secao_secoes_agregadas.add(secao_filho)
                    secao.principal = False
                    secao.save()
                secao_principal.secao_secoes_agregadas.add(secao)
            secao_principal.principal = True
            secao_principal.save()
            return NotifyResponse('Sucesso', theme='sucesso')    
    except Exception, e:
        return NotifyResponse('Erro ao desagregar', theme='erro', lista=[e.message,])
    return NotifyResponse('formulario não válido', theme='erro')

def secao_desagregar(request, id_secao):
    if not request.is_ajax():
        raise PermissionDenied
    secao = Secao.objects.get(pk=int(id_secao))
    try:
        secao.desagregarSecoes()
    except Exception, e:
        return NotifyResponse('Erro ao desagregar', theme='erro', lista=[e.message,])
    return NotifyResponse('Desagregação feita com sucesso', theme='sucesso')
