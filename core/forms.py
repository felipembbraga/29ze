'''
Created on 04/08/2014

@author: felipe

'''
from django import forms
from models import Local

class CarroImportarForm(forms.Form):
    arquivo = forms.FileField(
                              help_text=u'Entre com o arquivo no formato CSV ou TXT, com id e nome da marca, id e nome do modelo',
                              widget=forms.ClearableFileInput(attrs={'accept':'text/csv,text/plain'})
                              )
    
    
class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
    def __init__(self, *args, **kwargs):
        super(LocalForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            if not isinstance(self.fields[key].widget, forms.CheckboxInput):
                self.fields[key].widget.attrs.update({'class': 'form-control'})
