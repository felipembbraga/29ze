#-*- coding: utf-8 -*-

from django.contrib import messages
from django.shortcuts import render, redirect
from forms import OrgaoPublicoForm
from models import OrgaoPublico
from django.contrib.auth.decorators import login_required

@login_required(login_url='acesso:login-veiculos')
def orgao_atualizar(request):
    if not isinstance(request.user, OrgaoPublico):
        messages.error(request, 'Acesso apenas para órgãos.')
        redirect('home')
    if request.method == 'POST':
        form = OrgaoPublicoForm(request.POST, instance=request.user)
        if form.is_valid():
            orgao = form.save(commit=False)
            orgao.atualizar=False
            orgao.save()
            messages.success(request, 'Dados do órgão editados com sucesso.')
            return redirect('veiculos_index')
    else:
        form = OrgaoPublicoForm(instance=request.user)
    return render(request, 'acesso/orgao_publico/form.html', locals())