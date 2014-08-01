#-*- coding: utf-8 -*-
'''
Created on 30/07/2014

@author: felipe
'''

from django.contrib import messages
from django.shortcuts import redirect

def eleicao_required(func):
    def funcao(*args, **kwargs):
        request = args[0]
        if not request.eleicao_atual:
            messages.error(request, 'Cadastre uma eleição primeiro.')
            return redirect('home')
        return func(*args, **kwargs)
    return funcao