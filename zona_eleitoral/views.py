from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    if request.user.is_orgao():
        return redirect('veiculos:index')
    titulo = u'Seja Bem Vindo'
    return render(request, 'home.html', locals())
