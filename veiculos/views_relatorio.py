#-*- coding: utf-8 -*-
'''
Created on 07/08/2014

@author: felipe
'''
from django.forms.models import modelform_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from models import Veiculo, VeiculoSelecionado
from acesso.models import OrgaoPublico

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
    