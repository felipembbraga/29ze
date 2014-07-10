from django import forms
from models import Eleicao
from utils.forms import BootstrapModelForm


class EleicaoForm(BootstrapModelForm):
    
    class Meta:
        model = Eleicao
        exclude = ['eleitores','locais']
        
    

