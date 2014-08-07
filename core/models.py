#-*- coding: utf-8 -*-
from django.db import models
import datetime

# Create your models here.

class Pessoa(models.Model):
    u'''
    Classe referente aos dados gerais de Pessoa física
    '''
    titulo_eleitoral = models.CharField(u'Título Eleitoral', max_length=12, unique=True)
    nome = models.CharField('Nome do eleitor', max_length=100)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    endereco = models.CharField(u'Endereço Residencial', max_length=150, null=True, blank=True)
    cep = models.CharField('CEP', max_length=9, null=True, blank=True)
    telefone = models.CharField('Telefone', max_length=11, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    data_cadastro = models.DateTimeField(default=datetime.datetime.now())
    
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

