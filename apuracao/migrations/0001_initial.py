# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cidade'
        db.create_table(u'apuracao_cidade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codigo', self.gf('django.db.models.fields.IntegerField')()),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('uf', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('secoes', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'apuracao', ['Cidade'])

        # Adding model 'Apuracao'
        db.create_table(u'apuracao_apuracao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cidade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apuracao.Cidade'])),
            ('secoes_totalizadas', self.gf('django.db.models.fields.IntegerField')()),
            ('secoes_restantes', self.gf('django.db.models.fields.IntegerField')()),
            ('percentual', self.gf('django.db.models.fields.FloatField')()),
            ('dt_atualizacao', self.gf('django.db.models.fields.DateTimeField')()),
            ('finalizado', self.gf('django.db.models.fields.BooleanField')()),
            ('turno', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'apuracao', ['Apuracao'])


    def backwards(self, orm):
        # Deleting model 'Cidade'
        db.delete_table(u'apuracao_cidade')

        # Deleting model 'Apuracao'
        db.delete_table(u'apuracao_apuracao')


    models = {
        u'apuracao.apuracao': {
            'Meta': {'object_name': 'Apuracao'},
            'cidade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apuracao.Cidade']"}),
            'dt_atualizacao': ('django.db.models.fields.DateTimeField', [], {}),
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