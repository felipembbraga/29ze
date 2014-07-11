from django import forms
from models import Eleicao
from utils.forms import BootstrapModelForm, BootstrapForm

class EleicaoForm(BootstrapModelForm):
    
    class Meta:
        model = Eleicao
        exclude = ['eleitores','locais']


class LocalImportarForm(forms.Form):
    nome = forms.CharField()
    arquivo = forms.FileField(
                              help_text='Entre com o arquivo no formato CSV ou TXT',
                              widget=forms.ClearableFileInput(attrs={'accept':'text/csv,text/plain'})
                              )