from django.shortcuts import render, redirect
from forms import CarroImportarForm
from utils.importar_fipe import importar_tabela_fipe
# Create your views here.

def carro_importar(request):
    titulo = u'Importar Tabela FIPE'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CarroImportarForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            if importar_tabela_fipe(request.FILES['arquivo']):
                return redirect('home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CarroImportarForm()
    return render(request, 'core/veiculos/importar.html', locals())