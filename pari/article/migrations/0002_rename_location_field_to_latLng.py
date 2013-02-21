# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('article_location', 'location', 'latLng')

    def backwards(self, orm):
        db.rename_column('article_location', 'latLng', 'location')
