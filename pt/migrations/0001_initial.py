# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PtTest'
        db.create_table('PtTest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 9, 0, 0))),
            ('MsLevelFour', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pt', ['PtTest'])

        # Adding model 'PtScore'
        db.create_table('PtScore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pt_test', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['pt.PtTest'])),
        ))
        db.send_create_signal(u'pt', ['PtScore'])


    def backwards(self, orm):
        # Deleting model 'PtTest'
        db.delete_table('PtTest')

        # Deleting model 'PtScore'
        db.delete_table('PtScore')


    models = {
        u'pt.ptscore': {
            'Meta': {'object_name': 'PtScore', 'db_table': "'PtScore'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pt_test': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['pt.PtTest']"})
        },
        u'pt.pttest': {
            'Meta': {'object_name': 'PtTest', 'db_table': "'PtTest'"},
            'MsLevelFour': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 9, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['pt']