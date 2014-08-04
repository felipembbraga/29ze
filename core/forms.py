'''
Created on 04/08/2014

@author: felipe

'''
from django import forms

class CarroImportarForm(forms.Form):
    arquivo = forms.FileField(
                              help_text=u'Entre com o arquivo no formato CSV ou TXT, com id e nome da marca, id e nome do modelo',
                              widget=forms.ClearableFileInput(attrs={'accept':'text/csv,text/plain'})
                              )