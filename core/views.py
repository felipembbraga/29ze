#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from forms import CarroImportarForm
from utils.importar_fipe import importar_tabela_fipe
from core.models import Local
from core.forms import LocalForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# Create your views here.

def carro_importar(request):
    titulo = u'Importar Tabela FIPE'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CarroImportarForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            if importar_tabela_fipe(request.FILES['arquivo']):
                return redirect('home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CarroImportarForm()
    return render(request, 'core/veiculos/importar.html', locals())

def caminhao_importar(request):
    titulo = u'Importar Tabela FIPE para veículos pesados'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CarroImportarForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            if importar_tabela_fipe(request.FILES['arquivo'], True):
                return redirect('home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CarroImportarForm()
    return render(request, 'core/veiculos/importar.html', locals())

def local_listar(request):
    titulo = u'Locais'
    pesquisar = request.GET.get('pesquisar') and request.GET.get('pesquisar') or '' 
    if pesquisar != '':
        try:
            lista_locais = Local.objects.filter(\
                                                       Q(nome__icontains=pesquisar)|\
                                                       Q(id_local=int(pesquisar))).distinct('nome').order_by('nome')
        except ValueError:
            lista_locais = Local.objects.filter(nome__icontains=pesquisar).distinct('nome').order_by('nome')
    else:
        lista_locais = Local.objects.all().order_by('nome')
    for local in lista_locais:
        local.is_local_votacao = local.localvotacao_set.filter(eleicao=request.eleicao_atual).count() > 0 
        
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
    return render(request, 'core/local/listar.html', locals())

def local_cadastrar(request):
    if request.method == 'POST':
        form = LocalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('local-core:listar')
    else:
        form = LocalForm()
    return render(request, 'core/local/form.html', locals())
