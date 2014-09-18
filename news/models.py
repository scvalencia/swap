# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class News(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=4000)
    media = models.CharField(max_length=250)
    taken_from = models.CharField(max_length=50)
    created_at = models.DateField()
    class Meta:
        managed = False
        db_table = 'news'