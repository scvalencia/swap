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

class Vals(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    type = models.BigIntegerField()
    amount = models.BigIntegerField()
    availability = models.CharField(max_length=1)
    price = models.FloatField()
    active_login = models.ForeignKey(Actives, db_column='active_login')
    rent = models.ForeignKey(Rents)
    class Meta:
        managed = False
        db_table = 'vals'