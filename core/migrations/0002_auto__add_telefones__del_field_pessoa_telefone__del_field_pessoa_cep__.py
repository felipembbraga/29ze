# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Telefones'
        db.create_table(u'core_telefones', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pessoa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Pessoa'])),
            ('tel_residencial', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('tipo', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['Telefones'])

        # Deleting field 'Pessoa.telefone'
        db.delete_column(u'core_pessoa', 'telefone')

        # Deleting field 'Pessoa.cep'
        db.delete_column(u'core_pessoa', 'cep')

        # Deleting field 'Pessoa.data_nascimento'
        db.delete_column(u'core_pessoa', 'data_nascimento')

        # Deleting field 'Pessoa.email'
        db.delete_column(u'core_pessoa', 'email')


        # Changing field 'Pessoa.data_cadastro'
        db.alter_column(u'core_pessoa', 'data_cadastro', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):
        # Deleting model 'Telefones'
        db.delete_table(u'core_telefones')

        # Adding field 'Pessoa.telefone'
        db.add_column(u'core_pessoa', 'telefone',
                      self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Pessoa.cep'
        db.add_column(u'core_pessoa', 'cep',
                      self.gf('django.db.models.fields.CharField')(max_length=9, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Pessoa.data_nascimento'
        db.add_column(u'core_pessoa', 'data_nascimento',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Pessoa.email'
        db.add_column(u'core_pessoa', 'email',
                      self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Pessoa.data_cadastro'
        db.alter_column(u'core_pessoa', 'data_cadastro', self.gf('django.db.models.fields.DateTimeField')())

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
            'pessoa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Pessoa']"}),
            'tel_residencial': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']