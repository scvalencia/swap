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


class Contacts(models.Model):
    user_login = models.ForeignKey('actives.Actives', db_column='user_login', related_name='contacts(models.model):_user_login')
    link = models.CharField(max_length=50)
    name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'contacts'
