from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from acesso.models import OrgaoPublico
# Create your views here.

@login_required
def home(request):
    if isinstance(request.user, OrgaoPublico):
        return redirect('veiculos_index')
    titulo = u'Seja Bem Vindo'
    return render(request, 'home.html', locals())
