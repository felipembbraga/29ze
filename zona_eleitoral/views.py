from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from acesso.models import OrgaoPublico
from django.template import Context
from webodt.converters import converter
import webodt
import datetime
from webodt.shortcuts import render_to
# Create your views here.

@login_required
def home(request):
    if isinstance(request.user, OrgaoPublico):
        return redirect('veiculos_index')
    titulo = u'Seja Bem Vindo'
    return render(request, 'home.html', locals())

def index(request):
    return render(request, 'index.html')

def teste_odt(request):
    template = webodt.ODFTemplate('modelo_notificacao.odt')
    context = dict(data_alocacao = datetime.datetime.today(), balance=10.05)
    document = template.render(Context(context))
    conv = converter()
    pdf = conv.convert(document, format='pdf', output_filename='notificacao.pdf')
    return HttpResponse(pdf, mimetype='application/pdf')