# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Resource.date'
        db.add_column(u'resources_resource', 'date',
                      self.gf('django.db.models.fields.DateField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Resource.authors'
        db.add_column(u'resources_resource', 'authors',
                      self.gf('django.db.models.fields.TextField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Resource.focus'
        db.add_column(u'resources_resource', 'focus',
                      self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Resource.copyright'
        db.add_column(u'resources_resource', 'copyright',
                      self.gf('django.db.models.fields.TextField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Resource.thumbnail_url'
        db.add_column(u'resources_resource', 'thumbnail_url',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Resource.date'
        db.delete_column(u'resources_resource', 'date')

        # Deleting field 'Resource.authors'
        db.delete_column(u'resources_resource', 'authors')

        # Deleting field 'Resource.focus'
        db.delete_column(u'resources_resource', 'focus')

        # Deleting field 'Resource.copyright'
        db.delete_column(u'resources_resource', 'copyright')

        # Deleting field 'Resource.thumbnail_url'
        db.delete_column(u'resources_resource', 'thumbnail_url')


    models = {
        'resources.factoid': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Factoid'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'external_link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'factoids'", 'null': 'True', 'to': "orm['resources.Resource']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'resources.resource': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Resource'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'embed_source': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'focus': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'thumbnail_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['resources']