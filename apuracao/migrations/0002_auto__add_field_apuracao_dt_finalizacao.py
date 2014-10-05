# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Apuracao.dt_finalizacao'
        db.add_column(u'apuracao_apuracao', 'dt_finalizacao',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Apuracao.dt_finalizacao'
        db.delete_column(u'apuracao_apuracao', 'dt_finalizacao')


    models = {
        u'apuracao.apuracao': {
            'Meta': {'object_name': 'Apuracao'},
            'cidade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apuracao.Cidade']"}),
            'dt_atualizacao': ('django.db.models.fields.DateTimeField', [], {}),
            'dt_finalizacao': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'finalizado': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentual': ('django.db.models.fields.FloatField', [], {}),
            'secoes_restantes': ('django.db.models.fields.IntegerField', [], {}),
            'secoes_totalizadas': ('django.db.models.fields.IntegerField', [], {}),
            'turno': ('django.db.models.fields.IntegerField', [], {})
        },
        u'apuracao.cidade': {
            'Meta': {'object_name': 'Cidade'},
            'codigo': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'secoes': ('django.db.models.fields.IntegerField', [], {}),
            'uf': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['apuracao']