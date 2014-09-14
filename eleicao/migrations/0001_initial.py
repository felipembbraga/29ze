# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Eleicao'
        db.create_table(u'eleicao_eleicao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('data_turno_1', self.gf('django.db.models.fields.DateField')()),
            ('data_turno_2', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('atual', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'eleicao', ['Eleicao'])

        # Adding model 'LocalVotacao'
        db.create_table(u'eleicao_localvotacao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eleicao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eleicao.Eleicao'])),
            ('local', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Local'])),
            ('equipe', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='local_equipe', null=True, to=orm['eleicao.Equipe'])),
        ))
        db.send_create_signal(u'eleicao', ['LocalVotacao'])

        # Adding model 'Secao'
        db.create_table(u'eleicao_secao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_secao', self.gf('django.db.models.fields.IntegerField')()),
            ('eleicao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eleicao.Eleicao'])),
            ('local_votacao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eleicao.LocalVotacao'])),
            ('num_eleitores', self.gf('django.db.models.fields.IntegerField')()),
            ('principal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('especial', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('secoes_agregadas', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='secao_secoes_agregadas', null=True, to=orm['eleicao.Secao'])),
        ))
        db.send_create_signal(u'eleicao', ['Secao'])

        # Adding unique constraint on 'Secao', fields ['num_secao', 'eleicao']
        db.create_unique(u'eleicao_secao', ['num_secao', 'eleicao_id'])

        # Adding model 'Eleitor'
        db.create_table(u'eleicao_eleitor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eleicao', self.gf('django.db.models.fields.related.ForeignKey')(related_name='eleitor_eleicao', to=orm['eleicao.Eleicao'])),
            ('eleitor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='eleitor_eleitor', to=orm['core.Pessoa'])),
            ('secao', self.gf('django.db.models.fields.related.ForeignKey')(related_name='eleitor_secao', to=orm['eleicao.Secao'])),
        ))
        db.send_create_signal(u'eleicao', ['Eleitor'])

        # Adding model 'Coligacao'
        db.create_table(u'eleicao_coligacao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('eleicao', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coligacao_eleicao', to=orm['eleicao.Eleicao'])),
        ))
        db.send_create_signal(u'eleicao', ['Coligacao'])

        # Adding model 'Partido'
        db.create_table(u'eleicao_partido', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sigla', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('prefixo', self.gf('django.db.models.fields.IntegerField')()),
            ('coligacao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eleicao.Coligacao'])),
            ('eleicao', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partido_eleicao', to=orm['eleicao.Eleicao'])),
        ))
        db.send_create_signal(u'eleicao', ['Partido'])

        # Adding model 'Equipe'
        db.create_table(u'eleicao_equipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('eleicao', self.gf('django.db.models.fields.related.ForeignKey')(related_name='equipe_eleicao', to=orm['eleicao.Eleicao'])),
        ))
        db.send_create_signal(u'eleicao', ['Equipe'])

        # Adding model 'Montagem'
        db.create_table(u'eleicao_montagem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('local', self.gf('django.db.models.fields.related.OneToOneField')(related_name='local_montagem', unique=True, to=orm['eleicao.LocalVotacao'])),
            ('turno', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ordem', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'eleicao', ['Montagem'])

        # Adding model 'Cargo'
        db.create_table(u'eleicao_cargo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('eleicao', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cargo_eleicao', to=orm['eleicao.Eleicao'])),
        ))
        db.send_create_signal(u'eleicao', ['Cargo'])

        # Adding model 'Funcionario'
        db.create_table(u'eleicao_funcionario', (
            (u'pessoa_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Pessoa'], unique=True, primary_key=True)),
            ('equipe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='funcionario_equipe', to=orm['eleicao.Equipe'])),
            ('cargo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='funcionario_cargo', to=orm['eleicao.Cargo'])),
            ('eleicao', self.gf('django.db.models.fields.related.ForeignKey')(related_name='funcionario_eleicao', to=orm['eleicao.Eleicao'])),
        ))
        db.send_create_signal(u'eleicao', ['Funcionario'])


    def backwards(self, orm):
        # Removing unique constraint on 'Secao', fields ['num_secao', 'eleicao']
        db.delete_unique(u'eleicao_secao', ['num_secao', 'eleicao_id'])

        # Deleting model 'Eleicao'
        db.delete_table(u'eleicao_eleicao')

        # Deleting model 'LocalVotacao'
        db.delete_table(u'eleicao_localvotacao')

        # Deleting model 'Secao'
        db.delete_table(u'eleicao_secao')

        # Deleting model 'Eleitor'
        db.delete_table(u'eleicao_eleitor')

        # Deleting model 'Coligacao'
        db.delete_table(u'eleicao_coligacao')

        # Deleting model 'Partido'
        db.delete_table(u'eleicao_partido')

        # Deleting model 'Equipe'
        db.delete_table(u'eleicao_equipe')

        # Deleting model 'Montagem'
        db.delete_table(u'eleicao_montagem')

        # Deleting model 'Cargo'
        db.delete_table(u'eleicao_cargo')

        # Deleting model 'Funcionario'
        db.delete_table(u'eleicao_funcionario')


    models = {
        u'core.local': {
            'Meta': {'object_name': 'Local'},
            'bairro': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id_local': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.pessoa': {
            'Meta': {'object_name': 'Pessoa'},
            'cep': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'data_cadastro': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 14, 0, 0)'}),
            'data_nascimento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'titulo_eleitoral': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'})
        },
        u'eleicao.cargo': {
            'Meta': {'object_name': 'Cargo'},
            'eleicao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cargo_eleicao'", 'to': u"orm['eleicao.Eleicao']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'eleicao.coligacao': {
            'Meta': {'object_name': 'Coligacao'},
            'eleicao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coligacao_eleicao'", 'to': u"orm['eleicao.Eleicao']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'eleicao.funcionario': {
            'Meta': {'object_name': 'Funcionario', '_ormbases': [u'core.Pessoa']},
            'cargo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'funcionario_cargo'", 'to': u"orm['eleicao.Cargo']"}),
            'eleicao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'funcionario_eleicao'", 'to': u"orm['eleicao.Eleicao']"}),
            'equipe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'funcionario_equipe'", 'to': u"orm['eleicao.Equipe']"}),
            u'pessoa_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Pessoa']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'eleicao.localvotacao': {
            'Meta': {'object_name': 'LocalVotacao'},
            'eleicao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eleicao.Eleicao']"}),
            'equipe': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'local_equipe'", 'null': 'True', 'to': u"orm['eleicao.Equipe']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Local']"})
        },
        u'eleicao.montagem': {
            'Meta': {'object_name': 'Montagem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_montagem'", 'unique': 'True', 'to': u"orm['eleicao.LocalVotacao']"}),
            'ordem': ('django.db.models.fields.IntegerField', [], {}),
            'turno': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'eleicao.partido': {
            'Meta': {'object_name': 'Partido'},
            'coligacao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eleicao.Coligacao']"}),
            'eleicao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partido_eleicao'", 'to': u"orm['eleicao.Eleicao']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'prefixo': ('django.db.models.fields.IntegerField', [], {}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
        }
    }

    complete_apps = ['eleicao']