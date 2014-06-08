# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Company.co'
        db.delete_column('Company', 'co_id')

        # Adding field 'Company.commanding_officer'
        db.add_column('Company', 'commanding_officer',
                      self.gf('django.db.models.fields.related.OneToOneField')(related_name='company_co', null=True, to=orm['eagletrack.Cadet'], blank=True, unique=True, db_index=False),
                      keep_default=False)

        # Adding field 'Company.first_sergeant'
        db.add_column('Company', 'first_sergeant',
                      self.gf('django.db.models.fields.related.OneToOneField')(related_name='company_firstsgt', null=True, to=orm['eagletrack.Cadet'], blank=True, unique=True, db_index=False),
                      keep_default=False)


        # Changing field 'Company.name'
        db.alter_column('Company', 'name', self.gf('django.db.models.fields.CharField')(max_length=10))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Company.co'
        raise RuntimeError("Cannot reverse this migration. 'Company.co' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Company.co'
        db.add_column('Company', 'co',
                      self.gf('django.db.models.fields.related.OneToOneField')(related_name='company_cadet', unique=True, to=orm['eagletrack.Cadet'], db_index=False),
                      keep_default=False)

        # Deleting field 'Company.commanding_officer'
        db.delete_column('Company', 'commanding_officer_id')

        # Deleting field 'Company.first_sergeant'
        db.delete_column('Company', 'first_sergeant_id')


        # Changing field 'Company.name'
        db.alter_column('Company', 'name', self.gf('django.db.models.fields.CharField')(max_length=2))

    models = {
        u'eagletrack.cadet': {
            'Meta': {'object_name': 'Cadet', 'db_table': "'Cadet'"},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'company': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['eagletrack.Company']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'gpa': ('django.db.models.fields.DecimalField', [], {'default': '4.0', 'max_digits': '3', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_company_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ms_grade': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'ms_level': ('django.db.models.fields.CharField', [], {'default': "'one'", 'max_length': '4'})
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
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'platoons': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'company_platoons'", 'null': 'True', 'db_index': 'False', 'to': u"orm['eagletrack.Platoon']"})
        },
        u'eagletrack.platoon': {
            'Meta': {'object_name': 'Platoon', '_ormbases': [u'eagletrack.Company']},
            u'company_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['eagletrack.Company']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['eagletrack']