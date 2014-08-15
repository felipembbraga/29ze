'''
Created on 07/08/2014

@author: felipe
'''
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from models import Veiculo
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