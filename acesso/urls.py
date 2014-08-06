#-*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from django.contrib.auth.views import login, logout_then_login
from forms import LoginForm, LoginVeiculosForm

urlpatterns = patterns('',
    url(r'^login/$',login, {
                            'template_name':'acesso/login.html',
                            'authentication_form': LoginForm ,
                            'current_app':'eleicao',
                            'extra_context': {'titulo': u'Zona Eleitoral'},
                            }, name='login'),
    url(r'^login/veiculos/$',login, {
                                     'template_name':'acesso/login.html',
                                     'redirect_field_name':'veiculos:index',
                                     'authentication_form': LoginVeiculosForm ,
                                     'current_app':'veiculos',
                                     'extra_context': {'titulo': u'Cadastro de veículos'},
                                     }, name='login-veiculos'),
    url(r'^logout/$',logout_then_login, {'current_app':'eleicao'}, name='logout'),
    url(r'^logout-veiculos/$',logout_then_login, {'login_url':'acesso:login-veiculos'}, name='logout-veiculos'),
    
    
)