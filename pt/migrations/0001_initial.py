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
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 12, 0, 0))),
            ('MsLevelFour', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pt', ['PtTest'])

        # Adding model 'PtScore'
        db.create_table('PtScore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pt_test', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['pt.PtTest'])),
            ('cadet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='score_to_cadet', to=orm['eagletrack.Cadet'])),
        ))
        db.send_create_signal(u'pt', ['PtScore'])


    def backwards(self, orm):
        # Deleting model 'PtTest'
        db.delete_table('PtTest')

        # Deleting model 'PtScore'
        db.delete_table('PtScore')


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
            'pt_test': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['pt.PtTest']"})
        },
        u'pt.pttest': {
            'Meta': {'object_name': 'PtTest', 'db_table': "'PtTest'"},
            'MsLevelFour': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 12, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['pt']