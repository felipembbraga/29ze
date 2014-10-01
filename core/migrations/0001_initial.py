# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pessoa'
        db.create_table(u'core_pessoa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo_eleitoral', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('data_nascimento', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('endereco', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('cep', self.gf('django.db.models.fields.CharField')(max_length=9, null=True, blank=True)),
            ('telefone', self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('data_cadastro', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 10, 1, 0, 0))),
        ))
        db.send_create_signal(u'core', ['Pessoa'])

        # Adding model 'Local'
        db.create_table(u'core_local', (
            ('id_local', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('endereco', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('bairro', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'core', ['Local'])

        # Adding model 'Marca'
        db.create_table(u'core_marca', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Marca'])

        # Adding model 'Modelo'
        db.create_table(u'core_modelo', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('marca', self.gf('django.db.models.fields.related.ForeignKey')(related_name='modelo_marca', to=orm['core.Marca'])),
        ))
        db.send_create_signal(u'core', ['Modelo'])


    def backwards(self, orm):
        # Deleting model 'Pessoa'
        db.delete_table(u'core_pessoa')

        # Deleting model 'Local'
        db.delete_table(u'core_local')

        # Deleting model 'Marca'
        db.delete_table(u'core_marca')

        # Deleting model 'Modelo'
        db.delete_table(u'core_modelo')


    models = {
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
            'cep': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'data_cadastro': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 1, 0, 0)'}),
            'data_nascimento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'titulo_eleitoral': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'})
        }
    }

    complete_apps = ['core']