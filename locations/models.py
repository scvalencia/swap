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

class Locations(models.Model):
    user_login = models.ForeignKey(Actives, db_column='user_login', primary_key=True)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    department = models.CharField(max_length=20)
    gmt = models.CharField(max_length=10)
    address = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=10)
    class Meta:
        managed = False
        db_table = 'locations'