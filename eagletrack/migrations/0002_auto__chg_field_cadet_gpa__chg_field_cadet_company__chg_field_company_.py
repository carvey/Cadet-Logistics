# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Cadet.gpa'
        db.alter_column('Cadet', 'gpa', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2))

        # Changing field 'Cadet.company'
        db.alter_column('Cadet', 'company_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['eagletrack.Company'], unique=True, null=True))

        # Changing field 'Company.platoons'
        db.alter_column('Company', 'platoons_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['eagletrack.Platoon']))

    def backwards(self, orm):

        # Changing field 'Cadet.gpa'
        db.alter_column('Cadet', 'gpa', self.gf('django.db.models.fields.IntegerField')())

        # User chose to not deal with backwards NULL issues for 'Cadet.company'
        raise RuntimeError("Cannot reverse this migration. 'Cadet.company' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Cadet.company'
        db.alter_column('Cadet', 'company_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['eagletrack.Company'], unique=True))

        # User chose to not deal with backwards NULL issues for 'Company.platoons'
        raise RuntimeError("Cannot reverse this migration. 'Company.platoons' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Company.platoons'
        db.alter_column('Company', 'platoons_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eagletrack.Platoon']))

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
            'co': ('django.db.models.fields.related.OneToOneField', [], {'db_index': 'False', 'related_name': "'company_cadet'", 'unique': 'True', 'to': u"orm['eagletrack.Cadet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'alpha'", 'max_length': '2'}),
            'platoons': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'company_platoons'", 'null': 'True', 'db_index': 'False', 'to': u"orm['eagletrack.Platoon']"})
        },
        u'eagletrack.platoon': {
            'Meta': {'object_name': 'Platoon', '_ormbases': [u'eagletrack.Company']},
            u'company_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['eagletrack.Company']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['eagletrack']