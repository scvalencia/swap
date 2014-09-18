# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Typerents(models.Model):
    pk_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    function = models.BigIntegerField()
    length = models.BigIntegerField()
    rent_type = models.BigIntegerField()
    offerant_login = models.ForeignKey('offerants.Offerants', db_column='offerant_login', related_name='typerents(models.model):_offerant_login')

    class Meta:
        managed = False
        db_table = 'typerents'
