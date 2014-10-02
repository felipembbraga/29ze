# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from acesso.models import OrgaoPublico
from eleicao.models import Eleicao, LocalVotacao, Equipe
from core.models import Marca, Modelo, Local


tipo_veiculo_choices = list(enumerate(('Passeio', 'Caminhonete', u'Caminhão', u'Micro-ônibus', 'Moto' )))
estado_choices = list(enumerate((u'Ótimo', 'Bom', 'Regular', u'Sem condições de uso')))
ano_choices = [(i, i) for i in range(1990, datetime.date.today().year + 1)]


class Veiculo(models.Model):
    placa = models.CharField('Placa', max_length=8)
    marca = models.ForeignKey(Marca, verbose_name='Marca', related_name='veiculo_marca')
    modelo = models.ForeignKey(Modelo, verbose_name='Modelo', related_name='veiculo_modelo')
    tipo = models.IntegerField(u'Tipo de veículo', choices=tipo_veiculo_choices)
    lotacao = models.IntegerField(u'Lotação')
    ano = models.IntegerField(u'Ano de Fab.', choices=ano_choices)
    estado = models.IntegerField(u'Estado do veículo', choices=estado_choices)
    observacao = models.TextField('Observação', null=True, blank=True)
    orgao = models.ForeignKey(OrgaoPublico, related_name='veiculo_orgao')
    eleicao = models.ForeignKey(Eleicao, related_name='veiculo_eleicao')
    motorista_titulo_eleitoral = models.CharField(u'Título Eleitoral do Motorista', max_length=12, null=True)
    motorista_nome = models.CharField('Nome do Motorista', max_length=100, null=True)
    endereco = models.CharField(u'Endereço Residencial', max_length=150, null=True)
    tel_residencial = models.CharField('Telefone Residencial', max_length=14, null=True, blank=True)
    tel_celular = models.CharField('Telefone Celular', max_length=14, null=True)

    class Meta:
        verbose_name = u'Veículo'
        verbose_name_plural = u'Veículos'
        unique_together = ('placa', 'eleicao')
        permissions = (
            ('view_veiculo', u'Visualizar Veículos'),
            ('view_all_veiculo', u'Visualizar Todos os Veículos'),
            ('inspection_veiculo', u'Virtoria de Veículo'),
        )

    def __unicode__(self):
        return u'%s %s' % (self.marca.nome, self.modelo.nome)

    @models.permalink
    def get_absolute_url(self):
        return ('veiculo:editar', [str(self.pk)])

    def get_tipo(self):
        return dict(tipo_veiculo_choices).get(self.tipo)

    def get_estado(self):
        return dict(estado_choices).get(self.estado)

    def get_ano(self):
        return unicode(self.ano)

    def veiculo_with_popover(self):
        if self.observacao:
            html = u'''<span  class="tooltip-iniciar"
                href="#" data-toggle="tooltip" title="<label>Observação:&nbsp;</label>%(observacao)s">
                %(veiculo)s
                </span>'''

            return html % {'veiculo': unicode(self), 'observacao': self.observacao}
        return self.__unicode__()

    def save(self, *args, **kwargs):
        if hasattr(self, 'placa'):
            placa = getattr(self, 'placa')
            self.placa = placa.upper()
        if hasattr(self, 'nome_motorista'):
            nome = getattr(self, 'nome_motorista')
            self.nome_motorista = nome.upper()
        if hasattr(self, 'endereco'):
            endereco = getattr(self, 'endereco')
            self.endereco = endereco.upper()
        super(Veiculo, self).save(*args, **kwargs)


class VeiculoSelecionado(models.Model):
    """
    Veículo que foi requisitado pelo TRE
    Os campos local e administrador, no momento não estão sendo utilizados devido a mudança na lógica de cadastro
    """
    veiculo = models.OneToOneField(Veiculo, related_name='veiculo_selecionado')
    local = models.ForeignKey(LocalVotacao, related_name='local_veiculo', null=True, blank=True)
    administrador = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return unicode(self.veiculo)


class Motorista(models.Model):
    pessoa = models.ForeignKey('core.Pessoa')
    veiculo = models.ForeignKey(Veiculo, related_name='motorista_veiculo', null=True)
    eleicao = models.ForeignKey(Eleicao, related_name='motorista_eleicao')

    class Meta:
        verbose_name = u'Motorista'
        verbose_name_plural = u'Motoristas'
        unique_together = ('pessoa', 'eleicao')

    def __unicode__(self):
        return unicode(self.pessoa.nome)


class PerfilVeiculo(models.Model):
    nome = models.CharField(max_length=50)
    perfil_equipe = models.BooleanField(u'É perfil para equipe?', default=False)
    equipes = models.ManyToManyField(Equipe)

    def __unicode__(self):
        return unicode(self.nome)

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome=self.nome.upper()
        super(PerfilVeiculo, self).save(*args, **kwargs)

class CronogramaVeiculo(models.Model):
    perfil = models.ForeignKey(PerfilVeiculo, related_name="cronograma_perfil")
    local = models.ForeignKey(Local, null=True, blank=True, verbose_name=u'Local de Apresentação')
    dt_apresentacao = models.DateTimeField(u'Data da Apresentação')
    dia_montagem = models.BooleanField('Dia de montagem', default=False)
    eleicao = models.ForeignKey(Eleicao)


class Alocacao(models.Model):
    perfil_veiculo = models.ForeignKey(PerfilVeiculo)
    equipe = models.ForeignKey(Equipe)
    local_votacao = models.ForeignKey(LocalVotacao, null=True, blank=True)
    quantidade = models.PositiveIntegerField()

    class Meta:
        unique_together = ('perfil_veiculo', 'equipe', 'local_votacao')


class VeiculoAlocado(models.Model):
    veiculo = models.ForeignKey(Veiculo)
    perfil = models.ForeignKey(PerfilVeiculo)
    equipe = models.ForeignKey(Equipe)
    local_votacao = models.ForeignKey(LocalVotacao, null=True, blank=True)
    def __unicode__(self):
        return unicode(self.veiculo)


@receiver(post_save, sender=PerfilVeiculo)
def equipe_post_save(signal, instance, sender, **kwargs):

    for equipe in instance.equipes.all():
        if instance.perfil_equipe:
            if not Alocacao.objects.filter(perfil_veiculo=instance, equipe=equipe, local_votacao=None).exists():
                Alocacao.objects.create(perfil_veiculo=instance, equipe=equipe, local_votacao=None, quantidade=0)
            continue
        for local in equipe.local_equipe.all():
            if not Alocacao.objects.filter(perfil_veiculo=instance, equipe=equipe, local_votacao=local).exists():
                Alocacao.objects.create(perfil_veiculo=instance, equipe=equipe, local_votacao=local, quantidade=0)


def equipe_m2m_add(sender, instance, action, *args, **kwargs):
    for equipe in instance.equipes.all():
        if instance.perfil_equipe:
            if not Alocacao.objects.filter(perfil_veiculo=instance, equipe=equipe, local_votacao=None).exists():
                alocacao = Alocacao.objects.create(perfil_veiculo=instance, equipe=equipe, local_votacao=None, quantidade=0)
                alocacao.save()
            continue
        for local in equipe.local_equipe.all():
            if not Alocacao.objects.filter(perfil_veiculo=instance, equipe=equipe, local_votacao=local).exists():
                alocacao = Alocacao.objects.create(perfil_veiculo=instance, equipe=equipe, local_votacao=local, quantidade=0)
                alocacao.save()

m2m_changed.connect(equipe_m2m_add, sender=PerfilVeiculo.equipes.through)