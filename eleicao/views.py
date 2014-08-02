#-*- coding: utf-8 -*-
import csv
import json
from core.models import Local
from decorators import eleicao_required
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from forms import EleicaoForm, LocalImportarForm, EquipeForm, LocalEquipeForm, SecaoAgregarExternoForm
from models import Eleicao, LocalVotacao, Secao, Equipe
from middleware import definir_eleicao_padrao
from utils.Response import NotifyResponse
from django.contrib import messages



def javascript(request, nome_arquivo):
    return render(request, 'js/'+nome_arquivo, content_type='text/javascript')

def ler_csv(request, f):
    if request.eleicao_atual == None:
        messages.error(request, 'Cadastre uma eleição antes.')
        return False
    try:
        linhas = list(csv.reader(f, delimiter=','))
    except:
        messages.error(request, 'Erro ao importar o arquivo.')
        return False
    for linha in linhas[1:]:
        id_local, nome, endereco, bairro, secao, tipo_secao, num_eleitores = linha
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
            especial = False
            secao = Secao.objects.get(num_secao=int(secao), eleicao=request.eleicao_atual)
            secao.local_votacao, secao.num_eleitores = local_votacao, num_eleitores
            if tipo_secao.lower() == 'especial':
                especial = True
            secao.especial = especial
            secao.save()
        except:
            especial = False
            if tipo_secao.lower() == 'especial':
                especial = True
            secao = Secao.objects.create(\
                                         num_secao = int(secao),\
                                         eleicao = request.eleicao_atual,\
                                         local_votacao = local_votacao,\
                                         num_eleitores = num_eleitores,\
                                         especial = especial)
    return True

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
@eleicao_required
def local_importar(request):
    titulo = u'Importar Locais de Votação'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LocalImportarForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            if ler_csv(request, request.FILES['arquivo']):
                return redirect('local:index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LocalImportarForm()
    return render(request, 'eleicao/local_votacao/importar.html', locals())


@eleicao_required
def local_index(request):
    titulo = u'Locais de Votação'
    pesquisar = request.GET.get('pesquisar') and request.GET.get('pesquisar') or ''
    args = dict({'eleicao':request.eleicao_atual}) 
    if pesquisar != '':
        try:
            lista_locais = LocalVotacao.objects.filter(\
                                                       Q(local__nome__icontains=pesquisar)|\
                                                       Q(secao__num_secao=int(pesquisar))|\
                                                       Q(local__id_local=int(pesquisar)),
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

@eleicao_required
def local_definir_equipe(request, id_local):
    local = get_object_or_404(LocalVotacao, pk=int(id_local))
    titulo = u'Alterar equipe - ' + local.local.nome
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LocalEquipeForm(request, request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data['equipe'] == '':
                local.equipe = None
            else:
                equipe = get_object_or_404(Equipe, pk=int(form.cleaned_data['equipe']))
                local.equipe = equipe
            local.save()
            return redirect('local:detalhar', id_local)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LocalEquipeForm(request, {'equipe': local.equipe and local.equipe.pk or ''})
    return render(request, 'eleicao/local_votacao/definir_equipe.html', locals())

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

def secao_agregar_externo(request, id_secao):
    FormClass = SecaoAgregarExternoForm
    secao = get_object_or_404(Secao, pk=int(id_secao))
    titulo = u'Agregar seção %d a uma seção externa'%secao.num_secao
    locais = LocalVotacao.objects.exclude(pk=secao.local_votacao.pk)\
            .order_by('local__nome').values_list('local__pk', 'local__nome')
    if request.method == 'POST':
        FormClass.base_fields['secao'].choices += [(request.POST['secao'],'')]
        form = SecaoAgregarExternoForm(locais, request.POST)
        if form.is_valid():
            secao_agregada = Secao.objects.get(pk=int(form.cleaned_data['secao']))
            secao_principal = secao.num_eleitores >= secao_agregada.num_eleitores and secao or secao_agregada
            secao_filho = secao.num_eleitores < secao_agregada.num_eleitores and secao or secao_agregada
            if secao_filho.secao_secoes_agregadas.count() > 0:
                for s in secao_filho.secao_secoes_agregadas.all():
                    secao_principal.secao_secoes_agregadas.add(s)
                secao_filho.principal = False
            secao_principal.secao_secoes_agregadas.add(secao_filho)
            secao_principal.principal = True
            secao_principal.save()
            return redirect('local:detalhar', secao_principal.local_votacao.pk)
    else:
        form = SecaoAgregarExternoForm(locais)
    
    return render(request, 'eleicao/local_votacao/form.html', locals())
    
def secao_selecionar_secoes(request, id_local):
    #if not request.is_ajax():
    #    raise PermissionDenied
    secoes = Secao.objects.secao_pai()\
        .filter(local_votacao__local__pk=int(id_local)).order_by('num_secao')
    for secao in secoes:
        secao.nome = secao.unicode_agregadas()
    resposta = serializers.serialize('json', secoes, fields=('pk', 'num_secao', 'secoes_agregadas'))
    #raise Exception(resposta)
    return HttpResponse(resposta, mimetype='application/json')
    
@eleicao_required
def equipe_index(request):
    titulo = u'Equipes'
    equipes = Equipe.objects.filter(eleicao = request.eleicao_atual)
    return render(request, 'eleicao/equipe/index.html', locals())

@eleicao_required
def equipe_cadastrar(request):
    titulo = u'Cadastrar Equipe'
    if request.method == 'POST':
        
        equipe = Equipe(eleicao = request.eleicao_atual)
        form = EquipeForm(request.POST, instance=equipe)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect('equipe:index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EquipeForm()
    return render(request, 'eleicao/equipe/form.html', locals())

@eleicao_required
def equipe_editar(request, pk_equipe):
    titulo = u'Editar Equipe'
    equipe = get_object_or_404(Equipe, pk=int(pk_equipe))
    if request.method == 'POST':
        form = EquipeForm(request.POST, instance=equipe)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect('equipe:index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EquipeForm(instance=equipe)
    return render(request, 'eleicao/equipe/form.html', locals())