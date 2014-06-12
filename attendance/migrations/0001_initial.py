# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GenericEvent'
        db.create_table('GenericEvent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 12, 0, 0))),
            ('is_required', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
        ))
        db.send_create_signal(u'attendance', ['GenericEvent'])

        # Adding M2M table for field attended_list on 'GenericEvent'
        m2m_table_name = db.shorten_name('GenericEvent_attended_list')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('genericevent', models.ForeignKey(orm[u'attendance.genericevent'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['genericevent_id', 'user_id'])

        # Adding M2M table for field required_companies on 'GenericEvent'
        m2m_table_name = db.shorten_name('GenericEvent_required_companies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('genericevent', models.ForeignKey(orm[u'attendance.genericevent'], null=False)),
            ('company', models.ForeignKey(orm[u'eagletrack.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['genericevent_id', 'company_id'])

        # Adding M2M table for field required_ms_levels on 'GenericEvent'
        m2m_table_name = db.shorten_name('GenericEvent_required_ms_levels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('genericevent', models.ForeignKey(orm[u'attendance.genericevent'], null=False)),
            ('mslevel', models.ForeignKey(orm[u'eagletrack.mslevel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['genericevent_id', 'mslevel_id'])

        # Adding model 'PtEvent'
        db.create_table('PtEvent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 12, 0, 0))),
            ('is_required', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'attendance', ['PtEvent'])

        # Adding M2M table for field attended_list on 'PtEvent'
        m2m_table_name = db.shorten_name('PtEvent_attended_list')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ptevent', models.ForeignKey(orm[u'attendance.ptevent'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ptevent_id', 'user_id'])

        # Adding M2M table for field required_companies on 'PtEvent'
        m2m_table_name = db.shorten_name('PtEvent_required_companies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ptevent', models.ForeignKey(orm[u'attendance.ptevent'], null=False)),
            ('company', models.ForeignKey(orm[u'eagletrack.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ptevent_id', 'company_id'])

        # Adding M2M table for field required_ms_levels on 'PtEvent'
        m2m_table_name = db.shorten_name('PtEvent_required_ms_levels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ptevent', models.ForeignKey(orm[u'attendance.ptevent'], null=False)),
            ('mslevel', models.ForeignKey(orm[u'eagletrack.mslevel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ptevent_id', 'mslevel_id'])

        # Adding model 'LabEvent'
        db.create_table('LabEvent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 12, 0, 0))),
            ('is_required', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'attendance', ['LabEvent'])

        # Adding M2M table for field attended_list on 'LabEvent'
        m2m_table_name = db.shorten_name('LabEvent_attended_list')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('labevent', models.ForeignKey(orm[u'attendance.labevent'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['labevent_id', 'user_id'])

        # Adding M2M table for field required_companies on 'LabEvent'
        m2m_table_name = db.shorten_name('LabEvent_required_companies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('labevent', models.ForeignKey(orm[u'attendance.labevent'], null=False)),
            ('company', models.ForeignKey(orm[u'eagletrack.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['labevent_id', 'company_id'])

        # Adding M2M table for field required_ms_levels on 'LabEvent'
        m2m_table_name = db.shorten_name('LabEvent_required_ms_levels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('labevent', models.ForeignKey(orm[u'attendance.labevent'], null=False)),
            ('mslevel', models.ForeignKey(orm[u'eagletrack.mslevel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['labevent_id', 'mslevel_id'])

        # Adding model 'ClassEvent'
        db.create_table('ClassEvent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 12, 0, 0))),
            ('is_required', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'attendance', ['ClassEvent'])

        # Adding M2M table for field attended_list on 'ClassEvent'
        m2m_table_name = db.shorten_name('ClassEvent_attended_list')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('classevent', models.ForeignKey(orm[u'attendance.classevent'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['classevent_id', 'user_id'])

        # Adding M2M table for field required_companies on 'ClassEvent'
        m2m_table_name = db.shorten_name('ClassEvent_required_companies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('classevent', models.ForeignKey(orm[u'attendance.classevent'], null=False)),
            ('company', models.ForeignKey(orm[u'eagletrack.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['classevent_id', 'company_id'])

        # Adding M2M table for field required_ms_levels on 'ClassEvent'
        m2m_table_name = db.shorten_name('ClassEvent_required_ms_levels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('classevent', models.ForeignKey(orm[u'attendance.classevent'], null=False)),
            ('mslevel', models.ForeignKey(orm[u'eagletrack.mslevel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['classevent_id', 'mslevel_id'])

        # Adding model 'FtxEvent'
        db.create_table('FtxEvent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 12, 0, 0))),
            ('is_required', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'attendance', ['FtxEvent'])

        # Adding M2M table for field attended_list on 'FtxEvent'
        m2m_table_name = db.shorten_name('FtxEvent_attended_list')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ftxevent', models.ForeignKey(orm[u'attendance.ftxevent'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ftxevent_id', 'user_id'])

        # Adding M2M table for field required_companies on 'FtxEvent'
        m2m_table_name = db.shorten_name('FtxEvent_required_companies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ftxevent', models.ForeignKey(orm[u'attendance.ftxevent'], null=False)),
            ('company', models.ForeignKey(orm[u'eagletrack.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ftxevent_id', 'company_id'])

        # Adding M2M table for field required_ms_levels on 'FtxEvent'
        m2m_table_name = db.shorten_name('FtxEvent_required_ms_levels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ftxevent', models.ForeignKey(orm[u'attendance.ftxevent'], null=False)),
            ('mslevel', models.ForeignKey(orm[u'eagletrack.mslevel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ftxevent_id', 'mslevel_id'])


    def backwards(self, orm):
        # Deleting model 'GenericEvent'
        db.delete_table('GenericEvent')

        # Removing M2M table for field attended_list on 'GenericEvent'
        db.delete_table(db.shorten_name('GenericEvent_attended_list'))

        # Removing M2M table for field required_companies on 'GenericEvent'
        db.delete_table(db.shorten_name('GenericEvent_required_companies'))

        # Removing M2M table for field required_ms_levels on 'GenericEvent'
        db.delete_table(db.shorten_name('GenericEvent_required_ms_levels'))

        # Deleting model 'PtEvent'
        db.delete_table('PtEvent')

        # Removing M2M table for field attended_list on 'PtEvent'
        db.delete_table(db.shorten_name('PtEvent_attended_list'))

        # Removing M2M table for field required_companies on 'PtEvent'
        db.delete_table(db.shorten_name('PtEvent_required_companies'))

        # Removing M2M table for field required_ms_levels on 'PtEvent'
        db.delete_table(db.shorten_name('PtEvent_required_ms_levels'))

        # Deleting model 'LabEvent'
        db.delete_table('LabEvent')

        # Removing M2M table for field attended_list on 'LabEvent'
        db.delete_table(db.shorten_name('LabEvent_attended_list'))

        # Removing M2M table for field required_companies on 'LabEvent'
        db.delete_table(db.shorten_name('LabEvent_required_companies'))

        # Removing M2M table for field required_ms_levels on 'LabEvent'
        db.delete_table(db.shorten_name('LabEvent_required_ms_levels'))

        # Deleting model 'ClassEvent'
        db.delete_table('ClassEvent')

        # Removing M2M table for field attended_list on 'ClassEvent'
        db.delete_table(db.shorten_name('ClassEvent_attended_list'))

        # Removing M2M table for field required_companies on 'ClassEvent'
        db.delete_table(db.shorten_name('ClassEvent_required_companies'))

        # Removing M2M table for field required_ms_levels on 'ClassEvent'
        db.delete_table(db.shorten_name('ClassEvent_required_ms_levels'))

        # Deleting model 'FtxEvent'
        db.delete_table('FtxEvent')

        # Removing M2M table for field attended_list on 'FtxEvent'
        db.delete_table(db.shorten_name('FtxEvent_attended_list'))

        # Removing M2M table for field required_companies on 'FtxEvent'
        db.delete_table(db.shorten_name('FtxEvent_required_companies'))

        # Removing M2M table for field required_ms_levels on 'FtxEvent'
        db.delete_table(db.shorten_name('FtxEvent_required_ms_levels'))


    models = {
        u'attendance.classevent': {
            'Meta': {'object_name': 'ClassEvent', 'db_table': "'ClassEvent'"},
            'attended_list': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 12, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required_companies': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['eagletrack.Company']", 'symmetrical': 'False'}),
            'required_ms_levels': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['eagletrack.MsLevel']", 'symmetrical': 'False'})
        },
        u'attendance.ftxevent': {
            'Meta': {'object_name': 'FtxEvent', 'db_table': "'FtxEvent'"},
            'attended_list': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 12, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required_companies': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['eagletrack.Company']", 'symmetrical': 'False'}),
            'required_ms_levels': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['eagletrack.MsLevel']", 'symmetrical': 'False'})
        },
        u'attendance.genericevent': {
            'Meta': {'object_name': 'GenericEvent', 'db_table': "'GenericEvent'"},
            'attended_list': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 12, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'required_companies': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['eagletrack.Company']", 'symmetrical': 'False'}),
            'required_ms_levels': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['eagletrack.MsLevel']", 'symmetrical': 'False'})
        },
        u'attendance.labevent': {
            'Meta': {'object_name': 'LabEvent', 'db_table': "'LabEvent'"},
            'attended_list': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 12, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required_companies': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['eagletrack.Company']", 'symmetrical': 'False'}),
            'required_ms_levels': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['eagletrack.MsLevel']", 'symmetrical': 'False'})
        },
        u'attendance.ptevent': {
            'Meta': {'object_name': 'PtEvent', 'db_table': "'PtEvent'"},
            'attended_list': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 12, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required_companies': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['eagletrack.Company']", 'symmetrical': 'False'}),
            'required_ms_levels': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'to': u"orm['eagletrack.MsLevel']", 'symmetrical': 'False'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        }
    }

    complete_apps = ['attendance']