from django.conf.urls import include, url, patterns
from django.contrib.auth.views import login, logout_then_login

urlpatterns = patterns('',
    url(r'^login/$',login, {'template_name':'acesso/login.html', 'current_app':'eleicao'}, name='login'),
    url(r'^logout/$',logout_then_login, {'current_app':'eleicao'}, name='logout'),
    
    
)