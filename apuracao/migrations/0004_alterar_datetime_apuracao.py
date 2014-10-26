# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        import datetime
        from django.utils import timezone
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        for apuracao in orm.Apuracao.objects.all():
            apuracao.dt_atualizacao = timezone.make_aware(datetime.datetime(
                apuracao.dt_atualizacao.year,
                apuracao.dt_atualizacao.day,
                apuracao.dt_atualizacao.month,
                apuracao.dt_atualizacao.hour,
                apuracao.dt_atualizacao.minute,
                apuracao.dt_atualizacao.second,
                apuracao.dt_atualizacao.microsecond
            ), timezone.get_current_timezone())
            if apuracao.dt_finalizacao:
                apuracao.dt_finalizacao = timezone.make_aware(datetime.datetime(
                    apuracao.dt_finalizacao.year,
                    apuracao.dt_finalizacao.day,
                    apuracao.dt_finalizacao.month,
                    apuracao.dt_finalizacao.hour,
                    apuracao.dt_finalizacao.minute,
                    apuracao.dt_finalizacao.second,
                    apuracao.dt_finalizacao.microsecond
                ), timezone.get_current_timezone())
            apuracao.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'apuracao.apuracao': {
            'Meta': {'object_name': 'Apuracao'},
            'cidade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apuracao.Cidade']"}),
            'dt_atualizacao': ('django.db.models.fields.DateTimeField', [], {}),
            'dt_fechamento': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
    symmetrical = True
