#-*- coding: utf-8 -*-
from django import forms
from models import Eleicao
from utils.forms import BootstrapModelForm, BootstrapForm

class EleicaoForm(BootstrapModelForm):
    
    class Meta:
        model = Eleicao
        exclude = ['eleitores','locais']


class LocalImportarForm(forms.Form):
    arquivo = forms.FileField(
                              help_text=u'Entre com o arquivo no formato CSV ou TXT. O arquivo deve conter 6 colunas, com o id do local, nome do local, endereco, bairro, numero da seção e quantidade de pessoas na seção',
                              widget=forms.ClearableFileInput(attrs={'accept':'text/csv,text/plain'})
                              )
    
    
class SecaoAgregarForm(forms.Form):
    pk_secao = forms.MultipleChoiceField(widget  = forms.CheckboxSelectMultiple)