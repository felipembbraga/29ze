#-*- coding: utf-8 -*-
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from models import LocalVotacao, Equipe, Secao
from excel_response import ExcelResponse
from veiculos.models import VeiculoAlocado


@login_required
@permission_required('eleicao.view_local_votacao', raise_exception=True)
def relatorio_local_geral(request):
    locais = LocalVotacao.objects.filter(eleicao=request.eleicao_atual).order_by('local__nome').select_related()
    return render(request, 'eleicao/reports/local_geral.html', locals())


@permission_required('eleicao.view_equipe', raise_exception=True)
def relatorio_local_equipe(request):
    equipes = Equipe.objects.filter(eleicao=request.eleicao_atual).order_by('nome').select_related()
    return render(request, 'eleicao/reports/local_equipe.html', locals())


@permission_required('eleicao.view_equipe', raise_exception=True)
def relatorio_local_mala_direta(request):
    locais = LocalVotacao.objects.filter(eleicao=request.eleicao_atual).order_by('local__nome').select_related()
    cabecalho = ['equipe', 'num_local', 'nome_local', 'endereco', 'bairro', 'total_eleitores', 'secoes', 'total_secoes']
    data = [cabecalho,]
    max_secoes = 0
    for local in locais:
        if local.get_total_eleitores() == 0:
            continue
        equipe = local.equipe and local.equipe.nome or 'Sem equipe'
        num_local = local.local.id_local
        nome_local = local.local.nome
        endereco = local.local.endereco
        bairro = local.local.bairro
        total_eleitores = local.get_total_eleitores()
        secoes = local.get_secoes(delimitador='/')
        num_secoes = local.secao_set.secao_pai().count()
        lista = [equipe, num_local, nome_local, endereco, bairro, total_eleitores, secoes, num_secoes]
        total_secoes = local.secao_set.secao_pai()
        for secao in total_secoes:
            lista.append(secao.unicode_agregadas())
        data.append(lista)
        if len(total_secoes) > max_secoes:
            for i in range(1,len(total_secoes) + 1):
                if data[0].count('secao_' + str(i)) == 0:
                    data[0].append('secao_' + str(i))
            max_secoes = len(total_secoes)
            
    return ExcelResponse(data, 'locais_mala_direta')


def relatorio_local_mala_direta_por_secao(request):
    secoes = Secao.objects.secao_pai().filter(eleicao=request.eleicao_atual).order_by('num_secao').select_related()
    cabecalho = ['secao', 'equipe', 'num_local', 'nome_local', 'endereco', 'bairro', 'total_eleitores', 'secoes', 'total_secoes']
    data = [cabecalho,]
    for secao in secoes:
        if secao.local_votacao.get_total_eleitores() == 0:
            continue
        equipe = secao.local_votacao.equipe and secao.local_votacao.equipe.nome or 'Sem equipe'
        num_local = secao.local_votacao.local.id_local
        nome_local = secao.local_votacao.local.nome
        endereco = secao.local_votacao.local.endereco
        bairro = secao.local_votacao.local.bairro
        total_eleitores = secao.local_votacao.get_total_eleitores()
        secoes = secao.local_votacao.get_secoes(delimitador='/')
        num_secoes = secao.local_votacao.secao_set.secao_pai().count()
        lista = [secao.unicode_agregadas(), equipe, num_local, nome_local, endereco, bairro, total_eleitores, secoes, num_secoes]
        data.append(lista)

    return ExcelResponse(data, 'locais_mala_direta')


@permission_required('eleicao.view_local_votacao', raise_exception=True)
def relatorio_secao_ordenado(request):
    secoes = Secao.objects.filter(eleicao=request.eleicao_atual).order_by('num_secao')
    return render(request, 'eleicao/reports/secao_ordenado.html', locals())


@permission_required('eleicao.view_local_votacao', raise_exception=True)
def relatorio_secao_ordenado_xls(request):
    secoes = Secao.objects.filter(eleicao=request.eleicao_atual).order_by('num_secao')
    cabecalho = ['numero_secao', 'local', 'endereco', 'bairro']
    data = [cabecalho,]
    for secao in secoes:
        local = secao.get_local()
        if secao.secoes_agregadas:
            local += u'(agregada à seção %d)'%secao.secoes_agregadas.num_secao
        data.append([secao.num_secao, local, secao.get_endereco(), secao.get_bairro()])
            
    return ExcelResponse(data, 'secoes_ordenadas')


@permission_required('eleicao.view_local_votacao', raise_exception=True)
def relatorio_secoes_agregadas(request):
    secoes = Secao.objects.filter(eleicao=request.eleicao_atual, principal=True)
    return render(request, 'eleicao/reports/secoes-agregadas.html', locals())


@permission_required('eleicao.detail_equipe', raise_exception=True)
def relatorio_equipe(request, id_equipe):
    equipe = get_object_or_404(Equipe, pk=int(id_equipe))
    return render(request, 'eleicao/reports/equipe.html', locals())


def relatorio_equipe_rotas(request, id_equipe):
    equipe = get_object_or_404(Equipe, pk=int(id_equipe))
    return render(request, 'eleicao/reports/equipe_rotas.html', locals())


def relatorio_equipe_estimativa(request, id_equipe):
    equipe = get_object_or_404(Equipe, pk=int(id_equipe))
    return render(request, 'eleicao/reports/equipe_estimativa.html', locals())


def relatorio_estimativa_veiculos(request):
    equipes = Equipe.objects.filter(eleicao = request.eleicao_atual).order_by('nome')
    return render(request, 'eleicao/reports/estimativa.html', locals())
