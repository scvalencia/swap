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


class Solicitudes(models.Model):
    pk_id = models.CharField(primary_key=True, max_length=100)
    solicitude_type = models.BigIntegerField()
    amount = models.FloatField()
    created_at = models.DateField()
    total = models.FloatField()
    min_price = models.FloatField()
    bought = models.CharField(max_length=1)
    value = models.ForeignKey('vals.Vals', related_name='solicitudes(models.model):_value')
    active_login = models.ForeignKey('actives.Actives', db_column='active_login', related_name='solicitudes(models.model):_active_login')
    passive_login = models.ForeignKey('passives.Passives', db_column='passive_login', related_name='solicitudes(models.model):_passive_login')

    class Meta:
        managed = False
        db_table = 'solicitudes'
