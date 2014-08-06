from django.shortcuts import render
from forms import VeiculoForm, MotoristaForm
from models import Veiculo
# Create your views here.

def index(request):
    return render(request, 'veiculos/index.html')

def veiculo_cadastrar(request):
    if request.method == 'POST':
        v = Veiculo(orgao = request.user, eleicao=request.eleicao_atual)
        form = VeiculoForm(request.POST, instance = v)
        form_motorista = MotoristaForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('cadastrar_motorista'):
                if form_motorista.is_valid:
                    veiculo = form.save(commit=False)
                    motorista = form_motorista.save()
                    veiculo.motorista = motorista
                    veiculo.save()
            else:
                form.save()
    else:
        form = VeiculoForm()
        form_motorista = MotoristaForm()
    return render(request,'veiculos/veiculo/form.html', locals())