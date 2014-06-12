# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PtScore.pushups'
        db.add_column('PtScore', 'pushups',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'PtScore.situps'
        db.add_column('PtScore', 'situps',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'PtScore.two_mile'
        db.add_column('PtScore', 'two_mile',
                      self.gf('django.db.models.fields.TimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PtScore.pushups'
        db.delete_column('PtScore', 'pushups')

        # Deleting field 'PtScore.situps'
        db.delete_column('PtScore', 'situps')

        # Deleting field 'PtScore.two_mile'
        db.delete_column('PtScore', 'two_mile')


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
            'platoon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eagletrack.Platoon']", 'null': 'True', 'blank': 'True'}),
            'pt_scores': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'eagletrack_to_pt'", 'null': 'True', 'to': u"orm['pt.PtScore']"})
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
        },
        u'pt.ptscore': {
            'Meta': {'object_name': 'PtScore', 'db_table': "'PtScore'"},
            'cadet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'score_to_cadet'", 'to': u"orm['eagletrack.Cadet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pt_test': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['pt.PtTest']"}),
            'pushups': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'situps': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'two_mile': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pt.pttest': {
            'Meta': {'object_name': 'PtTest', 'db_table': "'PtTest'"},
            'MsLevelFour': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 12, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['pt']