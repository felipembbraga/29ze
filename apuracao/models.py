from django.db import models

# Create your models here.
from eleicao.models import Eleicao


class Cidade(models.Model):
    codigo =models.IntegerField()
    nome = models.CharField(max_length=80)
    uf = models.CharField(max_length=2)
    secoes = models.IntegerField()

class Apuracao(models.Model):
    cidade = models.ForeignKey(Cidade)
    secoes_totalizadas = models.IntegerField()
    secoes_restantes = models.IntegerField()
    percentual = models.DecimalField(max_digits=3, decimal_places=2)
    dt_atualizacao = models.DateTimeField()
    finalizado = models.BooleanField()
    turno = models.IntegerField()