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

class Follows(models.Model):
    follower_login = models.ForeignKey('Investors', db_column='follower_login')
    following_login = models.ForeignKey(Actives, db_column='following_login')
    class Meta:
        managed = False
        db_table = 'follows'