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
    
    @models.permalink
    def get_absolute_url(self):
        return ('eleicao:editar', [str(self.id)])
    
    def __unicode__(self):
        return self.nome
    
    def get_total_eleitores(self):
        return u'%(num_eleitores__sum)d' % self.secao_set.aggregate(models.Sum('num_eleitores'))
        

@receiver(post_save, sender=Eleicao)
def artigo_pre_save(signal, instance, sender, **kwargs):
    
    if instance.atual:
        sender.objects.exclude(pk=instance.pk).update(atual=False)


class LocalVotacao(models.Model):
    eleicao = models.ForeignKey(Eleicao)
    local = models.ForeignKey(Local)
    
    def __unicode__(self):
        return unicode(self.local.nome)
    
    def get_secoes(self):
        return u', '.join([unicode(s) for s in list(self.secao_set.all().order_by('num_secao'))])
    
    def get_total_eleitores(self):
        return u'%(num_eleitores__sum)d' % self.secao_set.aggregate(models.Sum('num_eleitores'))

    @models.permalink
    def get_absolute_url(self):
        return ('local:detalhar', [str(self.id)])
    
class SecaoManager(models.Manager):
    
    def secao_pai(self):
        return self.filter(secoes_agregadas=None).order_by('num_secao')
    
    def all_ordenado(self):
        return self.all().order_by('num_secao')
    
    
class Secao(models.Model):
    objects = SecaoManager()
    
    num_secao = models.IntegerField()
    eleicao = models.ForeignKey(Eleicao)
    local_votacao = models.ForeignKey(LocalVotacao)
    num_eleitores = models.IntegerField()
    principal = models.BooleanField(default=False)
    secoes_agregadas = models.ForeignKey('Secao', related_name='secao_secoes_agregadas', null=True, blank=True)
    
    class Meta:
        unique_together = ('num_secao', 'eleicao')
    
    def __unicode__(self):
        return unicode(self.num_secao)
    
    def desagregarSecoes(self):
        secoes = self.secao_secoes_agregadas.all()
        for secao in secoes:
            secao.secoes_agregadas = None
            secao.save()
        self.principal=False
        self.save()

    def secao_with_popover(self, principal=False):
        html = u'<span  class="tooltip-iniciar" href="#" data-toggle="tooltip" title="<label>Quantidade de eleitores: </label>%(num_eleitores)d">%(num_secao)s</span>'
        if self.principal or principal:
            return html%{'num_secao': '<strong>' +  str(self.num_secao)  + '</strong>', 'num_eleitores':self.num_eleitores}
        return html%{'num_secao':str(self.num_secao), 'num_eleitores':self.num_eleitores}
    
    def get_total_eleitores(self):
        total_agregado = self.secao_secoes_agregadas.aggregate(soma_agregados=models.Sum('num_eleitores'))
        return total_agregado['soma_agregados'] and self.num_eleitores + total_agregado['soma_agregados'] or self.num_eleitores
        
    def get_num_secao(self):
        agregadas = list(self.secao_secoes_agregadas.all_ordenado())
        if len(agregadas) == 0:
            return [self.secao_with_popover(True),]
        return [s.secao_with_popover() for s in ([self, ] + agregadas)]

    
class Eleitor(models.Model):
    eleicao = models.ForeignKey(Eleicao, related_name='eleitor_eleicao')
    eleitor = models.ForeignKey(Pessoa, related_name='eleitor_eleitor')
    secao = models.ForeignKey(Secao, related_name='eleitor_secao')
