# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table('Company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('commanding_officer', self.gf('django.db.models.fields.related.OneToOneField')(related_name='company_co', null=True, to=orm['eagletrack.Cadet'], blank=True, unique=True, db_index=False)),
            ('first_sergeant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='company_firstsgt', null=True, to=orm['eagletrack.Cadet'], blank=True, unique=True, db_index=False)),
        ))
        db.send_create_signal(u'eagletrack', ['Company'])

        # Adding model 'Cadet'
        db.create_table('Cadet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('age', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eagletrack.Company'], null=True, blank=True)),
            ('platoon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eagletrack.Platoon'], null=True, blank=True)),
            ('ms_level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eagletrack.MsLevel'])),
            ('gpa', self.gf('django.db.models.fields.DecimalField')(default=4.0, max_digits=3, decimal_places=2)),
            ('ms_grade', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_company_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'eagletrack', ['Cadet'])

        # Adding model 'Cadre'
        db.create_table('Cadre', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('age', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rank', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=75)),
        ))
        db.send_create_signal(u'eagletrack', ['Cadre'])

        # Adding model 'Platoon'
        db.create_table('Platoon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='1st Platoon', max_length=15)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='company', null=True, db_index=False, to=orm['eagletrack.Company'])),
        ))
        db.send_create_signal(u'eagletrack', ['Platoon'])

        # Adding model 'MsLevel'
        db.create_table('MsLevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'eagletrack', ['MsLevel'])


    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table('Company')

        # Deleting model 'Cadet'
        db.delete_table('Cadet')

        # Deleting model 'Cadre'
        db.delete_table('Cadre')

        # Deleting model 'Platoon'
        db.delete_table('Platoon')

        # Deleting model 'MsLevel'
        db.delete_table('MsLevel')


    models = {
        u'eagletrack.cadet': {
            'Meta': {'object_name': 'Cadet', 'db_table': "'Cadet'"},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eagletrack.Company']", 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'gpa': ('django.db.models.fields.DecimalField', [], {'default': '4.0', 'max_digits': '3', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_company_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ms_grade': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'ms_level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eagletrack.MsLevel']"}),
            'platoon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eagletrack.Platoon']", 'null': 'True', 'blank': 'True'})
        },
        u'eagletrack.cadre': {
            'Meta': {'object_name': 'Cadre', 'db_table': "'Cadre'"},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'eagletrack.company': {
            'Meta': {'object_name': 'Company', 'db_table': "'Company'"},
            'commanding_officer': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'company_co'", 'null': 'True', 'to': u"orm['eagletrack.Cadet']", 'blank': 'True', 'unique': 'True', 'db_index': 'False'}),
            'first_sergeant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'company_firstsgt'", 'null': 'True', 'to': u"orm['eagletrack.Cadet']", 'blank': 'True', 'unique': 'True', 'db_index': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'})
        },
        u'eagletrack.mslevel': {
            'Meta': {'object_name': 'MsLevel', 'db_table': "'MsLevel'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'eagletrack.platoon': {
            'Meta': {'object_name': 'Platoon', 'db_table': "'Platoon'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'company'", 'null': 'True', 'db_index': 'False', 'to': u"orm['eagletrack.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'1st Platoon'", 'max_length': '15'})
        }
    }

    complete_apps = ['eagletrack']