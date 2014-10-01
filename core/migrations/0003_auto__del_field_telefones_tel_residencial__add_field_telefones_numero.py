# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Telefones.tel_residencial'
        db.delete_column(u'core_telefones', 'tel_residencial')

        # Adding field 'Telefones.numero'
        db.add_column(u'core_telefones', 'numero',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=14),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Telefones.tel_residencial'
        db.add_column(u'core_telefones', 'tel_residencial',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=14),
                      keep_default=False)

        # Deleting field 'Telefones.numero'
        db.delete_column(u'core_telefones', 'numero')


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
            'data_cadastro': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'titulo_eleitoral': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'})
        },
        u'core.telefones': {
            'Meta': {'object_name': 'Telefones'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'pessoa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Pessoa']"}),
            'tipo': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']