#-*- coding: utf-8 -*-
from django.db import models
from core.models import Pessoa, Local
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Eleicao(models.Model):
    
    nome = models.CharField(u'Nome da eleição', max_length = 30)
    data_turno_1 = models.DateField('Data do primeiro turno')
    data_turno_2 = models.DateField('Data do segundo turno', null = True, blank = True)
    atual = models.BooleanField(default = True)
    eleitores = models.ManyToManyField(Pessoa, through = 'Eleitor', related_name='eleicao_eleitores')
    locais = models.ManyToManyField(Local, through = 'LocalVotacao', related_name='eleicao_locais')
    

@receiver(post_save, sender=Eleicao)
def artigo_pre_save(signal, instance, sender, **kwargs):
    if instance.atual:
        sender.objects.exclude(pk=instance.pk).update(atual=False)


class LocalVotacao(models.Model):
    eleicao = models.ForeignKey(Eleicao)
    local = models.ForeignKey(Local)
    
class Secao(models.Model):
    num_secao = models.IntegerField()
    local_votacao = models.ForeignKey(LocalVotacao)
    num_eleitores = models.IntegerField()
    principal = models.BooleanField(default=True)
    secoes_agregadas = models.ForeignKey('Secao', related_name='secao_secoes_agregadas', null=True, blank=True)
    
class Eleitor(models.Model):
    eleicao = models.ForeignKey(Eleicao, related_name='eleitor_eleicao')
    eleitor = models.ForeignKey(Pessoa, related_name='eleitor_eleitor')
    secao = models.ForeignKey(Secao, related_name='eleitor_secao')
