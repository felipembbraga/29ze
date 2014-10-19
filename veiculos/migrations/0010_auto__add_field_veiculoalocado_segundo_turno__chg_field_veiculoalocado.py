# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Motorista', fields ['pessoa', 'eleicao']
        db.delete_unique(u'veiculos_motorista', ['pessoa_id', 'eleicao_id'])

        # Removing unique constraint on 'VeiculoSelecionado', fields ['veiculo']
        db.delete_unique(u'veiculos_veiculoselecionado', ['veiculo_id'])

        # Removing unique constraint on 'Alocacao', fields ['perfil_veiculo', 'equipe', 'local_votacao']
        db.delete_unique(u'veiculos_alocacao', ['perfil_veiculo_id', 'equipe_id', 'local_votacao_id'])

        # Removing unique constraint on 'VeiculoAlocado', fields ['veiculo']
        db.delete_unique(u'veiculos_veiculoalocado', ['veiculo_id'])

        # Adding field 'VeiculoAlocado.segundo_turno'
        db.add_column(u'veiculos_veiculoalocado', 'segundo_turno',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'VeiculoAlocado.veiculo'
        db.alter_column(u'veiculos_veiculoalocado', 'veiculo_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['veiculos.Veiculo']))
        # Adding unique constraint on 'VeiculoAlocado', fields ['veiculo', 'segundo_turno']
        db.create_unique(u'veiculos_veiculoalocado', ['veiculo_id', 'segundo_turno'])

        # Adding field 'Alocacao.segundo_turno'
        db.add_column(u'veiculos_alocacao', 'segundo_turno',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding unique constraint on 'Alocacao', fields ['perfil_veiculo', 'equipe', 'local_votacao', 'segundo_turno']
        db.create_unique(u'veiculos_alocacao', ['perfil_veiculo_id', 'equipe_id', 'local_votacao_id', 'segundo_turno'])

        # Adding field 'CronogramaVeiculo.segundo_turno'
        db.add_column(u'veiculos_cronogramaveiculo', 'segundo_turno',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'VeiculoSelecionado.segundo_turno'
        db.add_column(u'veiculos_veiculoselecionado', 'segundo_turno',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'VeiculoSelecionado.veiculo'
        db.alter_column(u'veiculos_veiculoselecionado', 'veiculo_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['veiculos.Veiculo']))
        # Adding unique constraint on 'VeiculoSelecionado', fields ['veiculo', 'segundo_turno']
        db.create_unique(u'veiculos_veiculoselecionado', ['veiculo_id', 'segundo_turno'])

        # Adding field 'Motorista.segundo_turno'
        db.add_column(u'veiculos_motorista', 'segundo_turno',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding unique constraint on 'Motorista', fields ['pessoa', 'eleicao', 'segundo_turno']
        db.create_unique(u'veiculos_motorista', ['pessoa_id', 'eleicao_id', 'segundo_turno'])


    def backwards(self, orm):
        # Removing unique constraint on 'Motorista', fields ['pessoa', 'eleicao', 'segundo_turno']
        db.delete_unique(u'veiculos_motorista', ['pessoa_id', 'eleicao_id', 'segundo_turno'])

        # Removing unique constraint on 'VeiculoSelecionado', fields ['veiculo', 'segundo_turno']
        db.delete_unique(u'veiculos_veiculoselecionado', ['veiculo_id', 'segundo_turno'])

        # Removing unique constraint on 'Alocacao', fields ['perfil_veiculo', 'equipe', 'local_votacao', 'segundo_turno']
        db.delete_unique(u'veiculos_alocacao', ['perfil_veiculo_id', 'equipe_id', 'local_votacao_id', 'segundo_turno'])

        # Removing unique constraint on 'VeiculoAlocado', fields ['veiculo', 'segundo_turno']
        db.delete_unique(u'veiculos_veiculoalocado', ['veiculo_id', 'segundo_turno'])

        # Deleting field 'VeiculoAlocado.segundo_turno'
        db.delete_column(u'veiculos_veiculoalocado', 'segundo_turno')


        # Changing field 'VeiculoAlocado.veiculo'
        db.alter_column(u'veiculos_veiculoalocado', 'veiculo_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['veiculos.Veiculo'], unique=True))
        # Adding unique constraint on 'VeiculoAlocado', fields ['veiculo']
        db.create_unique(u'veiculos_veiculoalocado', ['veiculo_id'])

        # Deleting field 'Alocacao.segundo_turno'
        db.delete_column(u'veiculos_alocacao', 'segundo_turno')

        # Adding unique constraint on 'Alocacao', fields ['perfil_veiculo', 'equipe', 'local_votacao']
        db.create_unique(u'veiculos_alocacao', ['perfil_veiculo_id', 'equipe_id', 'local_votacao_id'])

        # Deleting field 'CronogramaVeiculo.segundo_turno'
        db.delete_column(u'veiculos_cronogramaveiculo', 'segundo_turno')

        # Deleting field 'VeiculoSelecionado.segundo_turno'
        db.delete_column(u'veiculos_veiculoselecionado', 'segundo_turno')


        # Changing field 'VeiculoSelecionado.veiculo'
        db.alter_column(u'veiculos_veiculoselecionado', 'veiculo_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['veiculos.Veiculo']))
        # Adding unique constraint on 'VeiculoSelecionado', fields ['veiculo']
        db.create_unique(u'veiculos_veiculoselecionado', ['veiculo_id'])

        # Deleting field 'Motorista.segundo_turno'
        db.delete_column(u'veiculos_motorista', 'segundo_turno')

        # Adding unique constraint on 'Motorista', fields ['pessoa', 'eleicao']
        db.create_unique(u'veiculos_motorista', ['pessoa_id', 'eleicao_id'])


    models = {
        u'acesso.orgaopublico': {
            'Meta': {'object_name': 'OrgaoPublico', '_ormbases': [u'auth.User']},
            'atualizar': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'data_expiracao': ('django.db.models.fields.DateField', [], {}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nome_secretaria': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'responsavel': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'responsavel_info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tel_celular': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'tel_comercial': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'tel_residencial': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.local': {
            'Meta': {'object_name': 'Local'},
            'bairro': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id_local': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.marca': {
            'Meta': {'object_name': 'Marca'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.modelo': {
            'Meta': {'object_name': 'Modelo'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'marca': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'modelo_marca'", 'to': u"orm['core.Marca']"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.pessoa': {
            'Meta': {'object_name': 'Pessoa'},
            'data_cadastro': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'titulo_eleitoral': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'})
        },
        u'eleicao.eleicao': {
            'Meta': {'object_name': 'Eleicao'},
            'atual': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'data_turno_1': ('django.db.models.fields.DateField', [], {}),
            'data_turno_2': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'eleitores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'eleicao_eleitores'", 'symmetrical': 'False', 'through': u"orm['eleicao.Eleitor']", 'to': u"orm['core.Pessoa']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locais': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'eleicao_locais'", 'symmetrical': 'False', 'through': u"orm['eleicao.LocalVotacao']", 'to': u"orm['core.Local']"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'eleicao.eleitor': {
            'Meta': {'object_name': 'Eleitor'},
            'eleicao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eleitor_eleicao'", 'to': u"orm['eleicao.Eleicao']"}),
            'eleitor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eleitor_eleitor'", 'to': u"orm['core.Pessoa']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'secao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eleitor_secao'", 'to': u"orm['eleicao.Secao']"})
        },
        u'eleicao.equipe': {
            'Meta': {'object_name': 'Equipe'},
            'eleicao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'equipe_eleicao'", 'to': u"orm['eleicao.Eleicao']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'eleicao.localvotacao': {
            'Meta': {'object_name': 'LocalVotacao'},
            'eleicao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eleicao.Eleicao']"}),
            'equipe': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'local_equipe'", 'null': 'True', 'to': u"orm['eleicao.Equipe']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Local']"})
        },
        u'eleicao.secao': {
            'Meta': {'unique_together': "(('num_secao', 'eleicao'),)", 'object_name': 'Secao'},
            'eleicao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eleicao.Eleicao']"}),
            'especial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_votacao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eleicao.LocalVotacao']"}),
            'num_eleitores': ('django.db.models.fields.IntegerField', [], {}),
            'num_secao': ('django.db.models.fields.IntegerField', [], {}),
            'principal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'secoes_agregadas': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'secao_secoes_agregadas'", 'null': 'True', 'to': u"orm['eleicao.Secao']"})
        },
        u'veiculos.alocacao': {
            'Meta': {'unique_together': "(('perfil_veiculo', 'equipe', 'local_votacao', 'segundo_turno'),)", 'object_name': 'Alocacao'},
            'equipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eleicao.Equipe']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_votacao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eleicao.LocalVotacao']", 'null': 'True', 'blank': 'True'}),
            'perfil_veiculo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['veiculos.PerfilVeiculo']"}),
            'quantidade': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'segundo_turno': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'veiculos.cronogramaveiculo': {
            'Meta': {'object_name': 'CronogramaVeiculo'},
            'dia_montagem': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dt_apresentacao': ('django.db.models.fields.DateTimeField', [], {}),
            'eleicao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eleicao.Eleicao']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Local']", 'null': 'True', 'blank': 'True'}),
            'perfil': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cronograma_perfil'", 'to': u"orm['veiculos.PerfilVeiculo']"}),
            'segundo_turno': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'veiculos.motorista': {
            'Meta': {'unique_together': "(('pessoa', 'eleicao', 'segundo_turno'),)", 'object_name': 'Motorista'},
            'eleicao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'motorista_eleicao'", 'to': u"orm['eleicao.Eleicao']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pessoa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Pessoa']"}),
            'segundo_turno': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'veiculo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'motorista_veiculo'", 'null': 'True', 'to': u"orm['veiculos.Veiculo']"})
        },
        u'veiculos.perfilveiculo': {
            'Meta': {'object_name': 'PerfilVeiculo'},
            'equipes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['eleicao.Equipe']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'perfil_equipe': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'veiculos.veiculo': {
            'Meta': {'unique_together': "(('placa', 'eleicao'),)", 'object_name': 'Veiculo'},
            'ano': ('django.db.models.fields.IntegerField', [], {}),
            'eleicao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'veiculo_eleicao'", 'to': u"orm['eleicao.Eleicao']"}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'estado': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lotacao': ('django.db.models.fields.IntegerField', [], {}),
            'marca': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'veiculo_marca'", 'to': u"orm['core.Marca']"}),
            'modelo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'veiculo_modelo'", 'to': u"orm['core.Modelo']"}),
            'motorista_nome': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'motorista_titulo_eleitoral': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'observacao': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'orgao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'veiculo_orgao'", 'to': u"orm['acesso.OrgaoPublico']"}),
            'placa': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'tel_celular': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True'}),
            'tel_residencial': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {})
        },
        u'veiculos.veiculoalocado': {
            'Meta': {'unique_together': "(('veiculo', 'segundo_turno'),)", 'object_name': 'VeiculoAlocado'},
            'equipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eleicao.Equipe']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_votacao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eleicao.LocalVotacao']", 'null': 'True', 'blank': 'True'}),
            'perfil': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['veiculos.PerfilVeiculo']"}),
            'segundo_turno': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'veiculo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['veiculos.Veiculo']"})
        },
        u'veiculos.veiculoselecionado': {
            'Meta': {'unique_together': "(('veiculo', 'segundo_turno'),)", 'object_name': 'VeiculoSelecionado'},
            'administrador': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'local_veiculo'", 'null': 'True', 'to': u"orm['eleicao.LocalVotacao']"}),
            'requisitado_vistoria': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'segundo_turno': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'veiculo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'veiculo_selecionado'", 'to': u"orm['veiculos.Veiculo']"})
        }
    }

    complete_apps = ['veiculos']