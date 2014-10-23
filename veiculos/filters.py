#-*- coding: utf-8 -*-
from django.db.models.query_utils import Q
from .models import Veiculo, ano_choices
from django import forms
import datetime
import django_filters
from veiculos.models import VeiculoAlocado


class FilterNullBooleanSelect(forms.NullBooleanSelect):
    def __init__(self, *args, **kwargs):
        super(FilterNullBooleanSelect, self).__init__(*args, **kwargs)
        self.choices = (('1', '-----------'),
                   ('2', 'Sim'),
                   ('3', u'Não'))
        
class FilterBooleanField(forms.NullBooleanField):
    widget = FilterNullBooleanSelect

class MyBooleanFilter(django_filters.BooleanFilter):
    field_class = FilterBooleanField
    
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
                    self.fields[key].choices = [('', '-----------'),] + list(self.fields[key].choices)

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
        return queryset.exclude(motorista_veiculo=None)
    else:
        return queryset.filter(motorista_veiculo=None)
    
def filter_selecionado(queryset, value):
    if value:
        return queryset.exclude(veiculo_selecionado=None).distinct()
    return queryset.filter(veiculo_selecionado=None)

def filter_selecionado_em_vistoria(queryset, value):
    if value:
        return queryset.filter(veiculo_selecionado__requisitado_vistoria=True).distinct()
    return queryset.exclude(veiculo_selecionado__requisitado_vistoria=True).distinct()

def filter_turno(queryset, value):
    if value=='1':
        return queryset.filter(veiculo_selecionado__segundo_turno=False).distinct()
    if value=='2':
        return queryset.filter(veiculo_selecionado__segundo_turno=True).distinct()
    return queryset

def filter_alocado(queryset, value):
    if value=='1':
        return queryset.filter(veiculoalocado__segundo_turno=False).distinct()
    if value=='2':
        return queryset.filter(veiculoalocado__segundo_turno=True).distinct()
    if value=='3':
        return queryset.exclude(veiculoalocado=None)
    if value=='4':
        return queryset.filter(Q(veiculoalocado__segundo_turno=True)&Q(veiculoalocado__segundo_turno=False)).distinct()
    if value=='5':
        if queryset.exists():
            primeiro = queryset.first()
            if not primeiro.veiculo_selecionado.exists() or primeiro.veiculo_selecionado.count() > 1:
                return queryset.filter(veiculoalocado=None)
            inicio = fim = primeiro.veiculo_selecionado.first().segundo_turno
            for veiculo in queryset[1:]:
                if not veiculo.veiculo_selecionado.exists() or veiculo.veiculo_selecionado.count() > 1:
                    fim = not inicio
                fim = veiculo.veiculo_selecionado.first().segundo_turno
                if inicio != fim:
                    break

            if inicio == fim:
                return queryset.filter(~Q(veiculoalocado__segundo_turno= inicio)|Q(veiculoalocado=None))
                lista_ids = []
                for veiculo in queryset:
                    if not veiculo.veiculoalocado_set.filter(segundo_turno=inicio).exists():
                        lista_ids.append(veiculo.pk)
                return Veiculo.objects.filter(pk__in=lista_ids)
        return queryset.filter(veiculoalocado=None)
    return queryset





class VeiculoFilter(django_filters.FilterSet):
    ano = django_filters.ChoiceFilter(choices=get_ano_choices(), action=filter_ano)
    motorista = MyBooleanFilter(action=filter_motorista)
    requisitado = MyBooleanFilter(action=filter_selecionado)
    turno = django_filters.ChoiceFilter(choices=((1,u'1º turno'),(2,u'2º turno')), action=filter_turno)
    requisitado_em_vistoria = MyBooleanFilter(action=filter_selecionado_em_vistoria)
    alocado = django_filters.ChoiceFilter(choices=(
        (1,u'Alocado no 1º turno'),(2,u'Alocado no 2º turno'), (3,u'Alocado no 1º ou 2º turno'), (4,u'Alocado no 1º e 2º turno')
    ), action=filter_alocado)

    class Meta:
        model = Veiculo
        fields = ['tipo', 'estado']
        form = FiltroForm


class FiltroVeiculoAlocadoForm(forms.ModelForm):
    class Meta:
        model = VeiculoAlocado
        fields=['perfil',]

    def __init__(self, *args, **kwargs):
        super(FiltroVeiculoAlocadoForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            if not isinstance(self.fields[key].widget, forms.CheckboxInput):
                self.fields[key].widget.attrs.update({'class': 'form-control'})
            if isinstance(self.fields[key].widget, forms.Select):
                if hasattr(self.fields[key], 'choices'):
                    self.fields[key].choices = [('', 'Selecione'),] + list(self.fields[key].choices)



class VeiculoAlocadoFilter(django_filters.FilterSet):


    class Meta:

        model = VeiculoAlocado
        fields = ['perfil__nome',]
        order_by = [('equipe', 'Equipe'), ('perfil', u'Função'), ('local_votacao', 'Local')]
        form = FiltroVeiculoAlocadoForm

    def get_ordering_field(self):
        field = super(VeiculoAlocadoFilter, self).get_ordering_field()
        field.label = 'Ordenar por'
        return field