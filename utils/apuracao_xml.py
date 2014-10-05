#-*- coding: utf-8 -*-
__author__ = 'felipe'


import zipfile
import os
from lxml import objectify
from dateutil import parser

def read_xml_from_zip(zipfile_name, xml_name):
    xml = ''
    if not zipfile.is_zipfile(zipfile_name):
        raise zipfile.BadZipfile('Arquivo não é um xml!')
    with zipfile.ZipFile(zipfile_name) as zf:
        xml += zf.read(xml_name)

    return xml

def get_capitais_from_xml(xml):
    dicionario = {}
    uf = xml.Br.Uf
    while uf is not None:
        municipio = uf.Municipio
        while municipio is not None:
            if municipio.attrib.get('capital') == 'S':
                dicionario[municipio.attrib['codigo']] = [uf.attrib['sigla'], municipio.attrib]
                break
            municipio = municipio.getnext()
        uf = uf.getnext()
    return dicionario

def get_percentual_apuracao(locais, xml):
    abrangencia = xml.Abrangencia
    lista = []
    while abrangencia is not None:
        cidade = locais.get(abrangencia.attrib['codigoAbrangencia'])
        if abrangencia.attrib['tipoAbrangencia'] == 'MU' and cidade is not None:
            dicionario = {}
            dicionario['cidade'] = int(cidade[1]['codigo'])
            dicionario['cidade'] = cidade[1]['nome']
            dicionario['UF'] = cidade[0]
            dicionario['secoes'] = int(cidade[1]['secoes']) + int(cidade[1]['secoesVT'])
            dicionario['secoes_totalizadas'] = float(abrangencia.attrib['secoesTotalizadas'])
            dicionario['secoes_restantes'] = int(abrangencia.attrib['secoesNaoTotalizadas'])
            dicionario['percentual'] = dicionario['secoes_totalizadas'] / dicionario['secoes']
            dicionario['dt_atualizacao'] = parser.parse('%s %s'%(abrangencia.attrib['dataTotalizacao'], abrangencia.attrib['horaTotalizacao']) )
            dicionario['finalizado'] = abrangencia.attrib['totalizacaoFinal'] == 'S' and True or False
            dicionario['turno'] = int(xml.attrib['turno'])
            lista.append(dicionario)
        abrangencia = abrangencia.getnext()
    return lista

def get_dados(xml_locais, xml_abrangencia, path_zip):
   xml = read_xml_from_zip('%s.zip'%os.path.join(path_zip,xml_locais), '%s.xml'%xml_locais)
   capitais = get_capitais_from_xml(objectify.fromstring(xml))
   xml_apuracao = read_xml_from_zip('%s.zip'%os.path.join(path_zip,xml_abrangencia), '%s.xml'%xml_abrangencia)
   return get_percentual_apuracao(capitais, objectify.fromstring(xml_apuracao))
