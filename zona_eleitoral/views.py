from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
# Create your views here.

def home(request):
    titulo = u'Seja Bem Vindo'
    return render(request, 'home.html', locals())
