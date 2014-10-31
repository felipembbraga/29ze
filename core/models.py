#-*- coding: utf-8 -*-
from django.db import models
import datetime
# Create your models here.
from django.db.models.expressions import F


class Pessoa(models.Model):
    u'''
    Classe referente aos dados gerais de Pessoa física
    '''
    titulo_eleitoral = models.CharField(u'Título Eleitoral', max_length=12, unique=True)
    nome = models.CharField('Nome do eleitor', max_length=100)
    endereco = models.CharField(u'Endereço Residencial', max_length=150, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def tel_residencial(self):
        return '/'.join(unicode(telefone) for telefone in self.telefones_set.filter(tipo=0))
    def tel_comercial(self):
        return '/'.join(unicode(telefone) for telefone in self.telefones_set.filter(tipo=1))
    def tel_celular(self):
        return '/'.join(unicode(telefone) for telefone in self.telefones_set.filter(tipo=2))

    def turnos_trabalhados(self):
        motoristas = self.motorista_set.filter(veiculo__veiculoalocado__isnull=False, veiculo__eleicao=F('eleicao')).distinct().order_by('segundo_turno')
        def turno(object):
            if object.segundo_turno:
                return u'2º'
            return u'1º'
        lista_turnos = map(turno, motoristas)
        return (motoristas.count() > 0 and ' e '.join(lista_turnos) + ' turno%s'%(motoristas.count()>1 and 's' or '') or 'Nenhum')

class Telefones(models.Model):
    pessoa = models.ForeignKey(Pessoa)
    numero = models.CharField(u'Número', max_length=14)
    tipo = models.IntegerField('Tipo', choices=[(0, 'Telefone residencial'), (1, 'Telefone comercial'), (2, 'Telefone celular')])

    def __unicode__(self):
        return unicode(self.numero)


class Local(models.Model):
    u'''
    Classe referente ao local registrado 
    '''
    id_local = models.IntegerField(primary_key = True)
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=150)
    bairro = models.CharField(max_length = 30)
    
    def get_id_local(self):
        return unicode(self.id_local)

    def __unicode__(self):
        return unicode(self.nome.upper())

#classes referente a veículos
class Marca(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.nome
        
class Modelo(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(u'Modelo do veículo', max_length = 100)
    marca = models.ForeignKey(Marca, verbose_name='Marca do veículo', related_name='modelo_marca')
    
    def __unicode__(self):
        return self.nome
    
    def unicode_completo(self):
        return u'%s %s'%(unicode(self.marca), unicode(self.nome))

