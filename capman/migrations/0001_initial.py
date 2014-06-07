# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'cadet'
        db.create_table('cadet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('ms_level', self.gf('django.db.models.fields.CharField')(default='one', max_length=4)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_company_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'capman', ['cadet'])

        # Adding model 'cadre'
        db.create_table('cadre', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('rank', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=75)),
        ))
        db.send_create_signal(u'capman', ['cadre'])


    def backwards(self, orm):
        # Deleting model 'cadet'
        db.delete_table('cadet')

        # Deleting model 'cadre'
        db.delete_table('cadre')


    models = {
        u'capman.cadet': {
            'Meta': {'object_name': 'cadet', 'db_table': "'cadet'"},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_company_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ms_level': ('django.db.models.fields.CharField', [], {'default': "'one'", 'max_length': '4'})
        },
        u'capman.cadre': {
            'Meta': {'object_name': 'cadre', 'db_table': "'cadre'"},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['capman']