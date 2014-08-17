#-*- coding: utf-8 -*-
from .models import Veiculo, ano_choices
from django import forms
import datetime
import django_filters


class FiltroForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields=['estado', 'tipo']
    
    def __init__(self, *args, **kwargs):
        super(FiltroForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            if not isinstance(self.fields[key].widget, forms.CheckboxInput):
                self.fields[key].widget.attrs.update({'class': 'form-control'})
            if isinstance(self.fields[key].widget, forms.Select):
                if hasattr(self.fields[key], 'choices'):
                    self.fields[key].choices = [('', 'Selecione'),] + list(self.fields[key].choices)

def get_ano_choices():
    ano_atual = datetime.date.today().year
    lista = []
    for i in range(1990, ano_atual + 1, 5):
        if ano_atual - i <= 5:
            lista.append((i, '%d a %d'%(i, ano_atual) ))
        else:
            lista.append((i, '%d a %d'%(i, i+4) ))
    return lista

def filter_ano(queryset, value):
    if value==u'':
        return queryset
    return queryset.filter(ano__gte=int(value), ano__lt=int(value)+5)

def filter_motorista(queryset, value):
    if value:
        return queryset.exclude(motorista_titulo_eleitoral=None)
    else:
        return queryset.filter(motorista_titulo_eleitoral=None)

class VeiculoFilter(django_filters.FilterSet):
    ano = django_filters.ChoiceFilter(choices=get_ano_choices(), action=filter_ano)
    motorista = django_filters.BooleanFilter(action=filter_motorista)
    class Meta:
        model = Veiculo
        fields = ['tipo', 'estado']
        form = FiltroForm