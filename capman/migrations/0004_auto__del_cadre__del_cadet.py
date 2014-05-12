# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'cadre'
        db.delete_table(u'capman_cadre')

        # Deleting model 'cadet'
        db.delete_table(u'capman_cadet')


    def backwards(self, orm):
        # Adding model 'cadre'
        db.create_table(u'capman_cadre', (
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('rank', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=75)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'capman', ['cadre'])

        # Adding model 'cadet'
        db.create_table(u'capman_cadet', (
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ms_level', self.gf('django.db.models.fields.CharField')(default='one', max_length=4)),
            ('is_company_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'capman', ['cadet'])


    models = {
        
    }

    complete_apps = ['capman']