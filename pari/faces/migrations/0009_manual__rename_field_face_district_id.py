# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column(u'faces_face', 'district_id_id', 'district_id')


    def backwards(self, orm):
        
        # The following code is provided here to aid in writing a correct migration
        db.rename_column(u'faces_face', 'district_id', 'district_id_id')
