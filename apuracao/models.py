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
        return u'%s - %s'()

class Apuracao(models.Model):
    cidade = models.ForeignKey(Cidade)
    secoes_totalizadas = models.IntegerField()
    secoes_restantes = models.IntegerField()
    percentual = models.DecimalField(max_digits=3, decimal_places=2)
    dt_atualizacao = models.DateTimeField()
    finalizado = models.BooleanField()
    turno = models.IntegerField()

def importar_dados():
    importacao = get_dados(settings.APURACAO_XML_LOCAIS, settings.APURACAO_XML_ABRANGENCIA, settings.APURACAO_PATH)
    for dicionario in importacao:
        cidade = Cidade.objects.get_or_create(codigo=dicionario['codigo'], nome=dicionario['cidade'], uf=dicionario['UF'], secoes=dicionario['secoes'])[0]
        print cidade
        apuracao = Apuracao.objects.get_or_create(cidade=cidade,
                                                  dt_atualizacao=dicionario['dt_atualizacao'],
                                                    secoes_totalizadas=dicionario['secoes_totalizadas'],
                                                     secoes_restantes=dicionario['secoes_restantes'],
                                                     percentual=dicionario['percentual'],
                                                     finalizado=dicionario['finalizado'],
                                                     turno = int(dicionario['turno'])
                                                     )

    return Cidade.objects.all().order_by('apuracao__percentual')







