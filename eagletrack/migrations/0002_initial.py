# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cadet'
        db.create_table('Cadet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('age', self.gf('django.db.models.fields.IntegerField')()),
            ('ms_level', self.gf('django.db.models.fields.CharField')(default='one', max_length=4)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_company_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'eagletrack', ['Cadet'])

        # Adding model 'Cadre'
        db.create_table('Cadre', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('age', self.gf('django.db.models.fields.IntegerField')()),
            ('rank', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=75)),
        ))
        db.send_create_signal(u'eagletrack', ['Cadre'])


    def backwards(self, orm):
        # Deleting model 'Cadet'
        db.delete_table('Cadet')

        # Deleting model 'Cadre'
        db.delete_table('Cadre')


    models = {
        u'eagletrack.cadet': {
            'Meta': {'object_name': 'Cadet', 'db_table': "'Cadet'"},
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_company_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ms_level': ('django.db.models.fields.CharField', [], {'default': "'one'", 'max_length': '4'})
        },
        u'eagletrack.cadre': {
            'Meta': {'object_name': 'Cadre', 'db_table': "'Cadre'"},
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['eagletrack']