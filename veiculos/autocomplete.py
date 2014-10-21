from acesso.models import OrgaoPublico
from core.models import Pessoa
from eleicao.models import EquipesAlocacao, LocalVotacao
from selectable.base import ModelLookup, LookupBase
from selectable.registry import registry
from veiculos.models import Marca, Modelo, Motorista, PerfilVeiculo, Alocacao
from django.db import models


class MotoristaLookup(ModelLookup):
    model = Pessoa
    search_fields = ('nome__icontains', 'titulo_eleitoral__icontains')
    filters = {'nome__isnull': False, 'titulo_eleitoral__isnull': False}

    def get_item_value(self, item):
        return "%s - %s" % (item.titulo_eleitoral, item.nome.upper())

    def get_item_label(self, item):
        return "%s - %s" % (item.titulo_eleitoral, item.nome.upper())

    def get_queryset(self):
        qs = self.model._default_manager.get_query_set()
        if self.filters:
            qs = qs.filter(**self.filters).order_by('nome')
        return qs


class OrgaoLookup(ModelLookup):
    model = OrgaoPublico
    search_fields = ('nome_secretaria__icontains', )

    def get_item_value(self, item):
        return "%s" % item.nome_secretaria

    def get_item_label(self, item):
        return "%s" % item.nome_secretaria


class MarcaLookup(ModelLookup):
    model = Marca
    search_fields = ('nome__icontains', )

    def get_item_value(self, item):
        return "%s" % item.nome

    def get_item_label(self, item):
        return "%s" % item.nome


class ModeloChainedMarcaLookup(ModelLookup, LookupBase):
    model = Modelo
    search_fields = ('nome__icontains', )

    def get_item_value(self, item):
        # Display for currently selected item
        return "%s" % item.nome

    def get_item_label(self, item):
        return "%s" % item.nome

    def get_query(self, request, term):
        results = super(ModeloChainedMarcaLookup, self).get_query(request, term)
        marca = request.GET.get('marca', '')
        if marca:
            results = results.filter(marca=marca).order_by('nome')
        return results


def equipes_c_vagas(equipe):
    return ((equipe.estimativa_equipe or 0) - equipe.veiculos_alocados_equipe) > 0


class EquipeLookup(ModelLookup):
    model = EquipesAlocacao
    search_fields = ('equipe__nome__icontains', )

    def get_item_value(self, item):
        return "%s" % item.equipe.nome

    def get_item_label(self, item):
        return "%s" % item.equipe.nome

    def get_query(self, request, term):
        qs = super(EquipeLookup, self).get_query(request, term)
        return filter(equipes_c_vagas, qs.order_by('equipe__nome'))


class PerfilChainedEquipeLookup(ModelLookup, LookupBase):
    model = PerfilVeiculo
    search_fields = ('nome__icontains', )

    def get_item_value(self, item):
        # Display for currently selected item
        return "%s" % item.nome

    def get_item_label(self, item):
        return "%s" % item.nome

    def get_query(self, request, term):
        results = super(PerfilChainedEquipeLookup, self).get_query(request, term)
        equipe = request.GET.get('equipe', '')

        if equipe:
            results = results.filter(equipes=equipe).order_by('nome')
            return results.filter(perfil_equipe=True)
        return []


def equipes_c_vagas_locais(equipe):
    return ((equipe.estimativa_local or 0) - equipe.veiculos_alocados_local) > 0


class EquipeManualLookup(ModelLookup):
    model = EquipesAlocacao
    search_fields = ('equipe__nome__icontains', )

    def get_item_value(self, item):
        return "%s" % item.equipe.nome

    def get_item_label(self, item):
        return "%s" % item.equipe.nome

    def get_query(self, request, term):
        qs = super(EquipeManualLookup, self).get_query(request, term)
        return filter(equipes_c_vagas_locais, qs.order_by('equipe__nome'))


def locais_c_vagas(local):
    soma_estimativa = local.alocacao_set.aggregate(models.Sum('quantidade')).get('quantidade__sum')
    total_veiculos = local.veiculoalocado_set.count()
    return soma_estimativa - total_veiculos > 0


class LocalManualChainedEquipeManualLookup(ModelLookup, LookupBase):
    model = LocalVotacao
    search_fields = ('local__nome__icontains', )

    def get_item_value(self, item):
        # Display for currently selected item
        return "%s" % item.local.nome

    def get_item_label(self, item):
        return "%s" % item.local.nome

    def get_query(self, request, term):
        results = super(LocalManualChainedEquipeManualLookup, self).get_query(request, term)
        equipe = request.GET.get('equipe_manual', '')
        if equipe:
            return filter(locais_c_vagas, results.filter(equipe=equipe).order_by('local__nome'))
        return []


def alocacao_c_vagas(alocacao):
    total_veiculos = alocacao.local_votacao.veiculoalocado_set.filter(perfil=alocacao.perfil_veiculo).count()
    return alocacao.quantidade - total_veiculos > 0


class PerfilManualChainedLocalManualLookup(ModelLookup, LookupBase):
    model = Alocacao
    search_fields = ('perfil_veiculo__nome__icontains', )

    def get_item_value(self, item):
        # Display for currently selected item
        return "%s" % item.perfil_veiculo.nome

    def get_item_label(self, item):
        return "%s" % item.perfil_veiculo.nome

    def get_query(self, request, term):
        results = super(PerfilManualChainedLocalManualLookup, self).get_query(request, term)
        local = request.GET.get('local_manual', '')

        if local:
            return filter(alocacao_c_vagas, results.filter(local_votacao=local).order_by('perfil_veiculo__nome'))
        return []


registry.register(ModeloChainedMarcaLookup)
registry.register(OrgaoLookup)
registry.register(MarcaLookup)
registry.register(MotoristaLookup)
registry.register(EquipeLookup)
registry.register(PerfilChainedEquipeLookup)
registry.register(EquipeManualLookup)
registry.register(LocalManualChainedEquipeManualLookup)
registry.register(PerfilManualChainedLocalManualLookup)
