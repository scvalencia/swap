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


class Transactions(models.Model):
    pk_id = models.CharField(primary_key=True, max_length=20)
    created_at = models.DateField()
    passive_login = models.ForeignKey('passives.Passives', db_column='passive_login', related_name='transactions(models.model):_passive_login')
    active_login = models.ForeignKey('actives.Actives', db_column='active_login', related_name='transactions(models.model):_active_login')
    solved_request = models.ForeignKey('solicitudes.Solicitudes', related_name='transactions(models.model):_solved_request')
    sold_request = models.ForeignKey('solicitudes.Solicitudes', related_name='transactions(models.model):_sold_request')

    class Meta:
        managed = False
        db_table = 'transactions'
