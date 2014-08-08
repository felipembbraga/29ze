#-*- coding: utf-8 -*-
'''
Created on 30/07/2014

@author: felipe
'''

from django.contrib import messages
from django.shortcuts import redirect
from models import OrgaoPublico

def orgao_atualizar(func):
    def funcao(*args, **kwargs):
        request = args[0]
        if isinstance(request.user, OrgaoPublico):
            if request.user.atualizar:
                messages.error(request, 'Atualize seus dados.')
                return redirect('acesso:orgao-atualizar')
        return func(*args, **kwargs)
    return funcao