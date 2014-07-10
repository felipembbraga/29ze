from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from forms import EleicaoForm
from models import Eleicao

# Create your views here.

def eleicao_cadastrar(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EleicaoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect('eleicao:index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EleicaoForm()

    return render(request, 'eleicao/eleicao/cadastrar.html', {'form': form})
    
def eleicao_index(request):
    eleicoes = Eleicao.objects.all()
    return render(request, 'eleicao/eleicao/index.html', locals())

def local_importar(request):
    return render(request, 'eleicao/local/importar.html')
