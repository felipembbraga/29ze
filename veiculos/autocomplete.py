from eleicao.models import EquipesAlocacao
from selectable.base import ModelLookup, LookupBase
from selectable.registry import registry
from veiculos.models import Marca, Modelo, Veiculo, Motorista, PerfilVeiculo


class MotoristaLookup(ModelLookup):
    model = Motorista
    search_fields = ('pessoa__nome__icontains', 'pessoa__titulo_eleitoral__icontains')
    filters = {'pessoa__nome__isnull': False, 'pessoa__titulo_eleitoral__isnull': False}

    def get_item_value(self, item):
        return "%s - %s" % (item.pessoa.titulo_eleitoral, item.pessoa.nome.upper())

    def get_item_label(self, item):
        return "%s - %s" % (item.pessoa.titulo_eleitoral, item.pessoa.nome.upper())

    def get_queryset(self):
        qs = self.model._default_manager.get_query_set()
        if self.filters:
            qs = qs.filter(**self.filters).order_by('pessoa__nome')
        return qs


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
    return (equipe.estimativa_equipe or 0 - equipe.veiculos_alocados_equipe) > 0

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


registry.register(ModeloChainedMarcaLookup)
registry.register(MarcaLookup)
registry.register(MotoristaLookup)
registry.register(EquipeLookup)
registry.register(PerfilChainedEquipeLookup)