# -*- coding: utf-8 -*-
'''
Created on 05/08/2014

@author: felipe
'''
from django import forms
from models import Veiculo
from core.models import Marca

class VeiculoForm(forms.ModelForm):
    marca = forms.ModelChoiceField(queryset=Marca.objects.all().order_by('nome'))
    placa = forms.RegexField(
                        r'[A-Za-z]{3}-\d{4}',max_length=8, help_text='Ex.:ABC-1234', error_messages={'invalid' : u'Insira uma placa válida.'})
    cadastrar_motorista = forms.BooleanField(initial=False,label = 'Cadastrar Motorista para o Veículo',required=False)
    
    class Meta:
        model = Veiculo
        fields = ['placa', 'marca', 'modelo', 'ano', 'tipo', 'lotacao', 'estado', 'observacao']
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 3}),
        }
        
    
    def __init__(self, *args, **kwargs):
        super(VeiculoForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['placa'].widget = forms.HiddenInput()
        for key in self.fields:
            if not isinstance(self.fields[key].widget, forms.CheckboxInput):
                self.fields[key].widget.attrs.update({'class': 'form-control'})
    
    def clean_placa(self):
        if not self.instance.pk and Veiculo.objects.filter(placa=self.cleaned_data.get('placa'), eleicao=self.instance.eleicao).exists():
            raise forms.ValidationError(u'O veículo com esta placa já está cadastrado')
        return self.cleaned_data.get('placa')
    
    
class MotoristaForm(forms.ModelForm):
    motorista_titulo_eleitoral = forms.RegexField(r'\d{12}', label=u'Título Eleitoral do Motorista',max_length=12, help_text=u'Entre 11 e 12 dígitos.')
    
    class Meta:
        model = Veiculo
        fields = ['motorista_titulo_eleitoral', 'motorista_nome', 'endereco', 'tel_residencial', 'tel_celular']
        widgets = {
            'tel_residencial': forms.TextInput(attrs={'class': 'telefone'}),
            'tel_celular': forms.TextInput(attrs={'class': 'telefone'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(MotoristaForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            if not isinstance(self.fields[key].widget, forms.CheckboxInput):
                self.fields[key].widget.attrs.update({'class': self.fields[key].widget.attrs.get('class') and self.fields[key].widget.attrs.get('class') + ' form-control' or 'form-control'})
    
    