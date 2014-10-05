import datetime
from django.db import models
import os
from utils.apuracao_xml import get_dados
from django.conf import settings
# Create your models here.
from eleicao.models import Eleicao


class Cidade(models.Model):
    codigo =models.IntegerField()
    nome = models.CharField(max_length=80)
    uf = models.CharField(max_length=2)
    secoes = models.IntegerField()

    def __unicode__(self):
        return u'%s - %s'%(unicode(self.nome), unicode(self.uf))



class Apuracao(models.Model):
    cidade = models.ForeignKey(Cidade)
    secoes_totalizadas = models.IntegerField()
    secoes_restantes = models.IntegerField()
    percentual = models.FloatField()
    dt_atualizacao = models.DateTimeField()
    finalizado = models.BooleanField()
    dt_finalizacao = models.DateTimeField(null=True, blank=True)
    dt_fechamento = models.DateTimeField(null=True, blank=True)
    turno = models.IntegerField()

def importar_dados():
    importacao = get_dados(settings.APURACAO_XML_LOCAIS, settings.APURACAO_XML_ABRANGENCIA, settings.APURACAO_PATH)
    for dicionario in importacao:
        if Cidade.objects.filter(codigo=dicionario['codigo']).exists():
            cidade = Cidade.objects.get(codigo=dicionario['codigo'])
        else:
            cidade = Cidade.objects.create(codigo=dicionario['codigo'], nome=dicionario['cidade'], uf=dicionario['UF'], secoes=dicionario['secoes'])
            print cidade
        if Apuracao.objects.filter(cidade=cidade, dt_atualizacao=dicionario['dt_atualizacao']).exists():
            continue
        apuracao = Apuracao.objects.create(cidade=cidade,
                                                  dt_atualizacao=dicionario['dt_atualizacao'],
                                                    secoes_totalizadas=dicionario['secoes_totalizadas'],
                                                     secoes_restantes=dicionario['secoes_restantes'],
                                                     percentual=dicionario['percentual'],
                                                     finalizado=dicionario['finalizado'],
                                                     turno = int(dicionario['turno'])
                                                     )
        if apuracao.finalizado:
            apuracao.dt_fechamento = datetime.datetime.now()

        if not apuracao.dt_finalizacao and apuracao.percentual>=100:
            apuracao.dt_finalizacao = apuracao.dt_atualizacao
        apuracao.save()
    return Cidade.objects.all()







