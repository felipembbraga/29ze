#-*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from acesso.models import OrgaoPublico
from eleicao.models import Eleicao
from core.models import Marca, Modelo, Pessoa
import datetime

tipo_veiculo_choices = enumerate(('Passeio', 'Caminhonete', u'Caminhão', u'Micro-ônibus', 'Moto' ))
estado_choices = enumerate((u'Ótimo','Bom','Regular',u'Sem condições de uso'))
ano_choices = [(i,i) for i in range(1990, datetime.date.today().year + 1)]

class Veiculo(models.Model):
    placa = models.CharField('Placa', max_length=7)
    marca = models.ForeignKey(Marca, verbose_name='Marca', related_name='veiculo_marca')
    modelo = models.ForeignKey(Modelo, verbose_name='Modelo', related_name='veiculo_modelo')
    tipo = models.IntegerField(u'Tipo de veículo', choices = tipo_veiculo_choices)
    lotacao = models.IntegerField(u'Lotação máxima')
    ano = models.IntegerField(u'Ano de Fabricação', choices=ano_choices)
    estado = models.IntegerField(u'Estado do veículo', choices = estado_choices)
    observacao = models.TextField('Observação', null=True, blank=True)
    motorista = models.ForeignKey(Pessoa, verbose_name='Motorista', related_name='veiculo_motorista', blank=True, null=True)
    orgao = models.ForeignKey(OrgaoPublico, related_name='veiculo_orgao')
    eleicao = models.ForeignKey(Eleicao, related_name='veiculo_eleicao')
    
    class Meta:
        verbose_name= u'Veículo'
        verbose_name_plural= u'Veículos'
        permissions = (
                       ('view_veiculo', u'Visualizar Veículos'),
                       )
        