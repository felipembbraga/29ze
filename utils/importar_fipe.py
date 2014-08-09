#-*- coding: utf-8 -*-
'''
Created on 04/08/2014

@author: felipe
'''
import csv
from core.models import Marca, Modelo

def importar_tabela_fipe(csvfile, caminhao=False):
    
    reader = csv.reader(csvfile, delimiter=',')
    for linha in list(reader)[1:]:
        id_marca, nome_marca, id_modelo, nome_modelo = linha
        if caminhao:
            if Marca.objects.filter(nome__icontains=nome_marca):
                nome_marca +=' (Veículos pesados)'
        try:
            marca = Marca.objects.get(pk=int(id_marca))
        except:
            marca = Marca(id=int(id_marca), nome=nome_marca)
            marca.save()
        finally:
            if Modelo.objects.filter(pk=int(id_modelo.replace('-',''))).count() == 0:
                modelo = Modelo(id=int(id_modelo.replace('-','')), nome=nome_modelo, marca=marca)
                modelo.save()
    return True