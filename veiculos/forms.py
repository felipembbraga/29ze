'''
Created on 05/08/2014

@author: felipe
'''
from django import forms
from models import Veiculo
from core.models import Pessoa

class VeiculoForm(forms.ModelForm):
    cadastrar_motorista = forms.BooleanField(label='Cadastrar motorista')
    class Meta:
        model = Veiculo
        fields = ['placa', 'marca', 'modelo', 'ano', 'tipo', 'estado', 'observacao']
        
class MotoristaForm(forms.ModelForm):
    class Meta:
        model=Pessoa