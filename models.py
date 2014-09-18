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

class Actives(models.Model):
    user_login = models.ForeignKey('Users', db_column='user_login', primary_key=True)
    passive_register = models.ForeignKey('Passives', db_column='passive_register', unique=True)
    class Meta:
        managed = False
        db_table = 'actives'

class Comments(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    content = models.CharField(max_length=4000)
    created_at = models.DateField()
    news_title = models.ForeignKey('News', db_column='news_title')
    news_taken_from = models.ForeignKey('News', db_column='news_taken_from')
    user_login = models.ForeignKey(Actives, db_column='user_login')
    class Meta:
        managed = False
        db_table = 'comments'

class Contacts(models.Model):
    user_login = models.ForeignKey(Actives, db_column='user_login')
    link = models.CharField(max_length=50)
    name = models.CharField(max_length=10)
    class Meta:
        managed = False
        db_table = 'contacts'

class Follows(models.Model):
    follower_login = models.ForeignKey('Investors', db_column='follower_login')
    following_login = models.ForeignKey(Actives, db_column='following_login')
    class Meta:
        managed = False
        db_table = 'follows'

class Investors(models.Model):
    user_login = models.ForeignKey(Actives, db_column='user_login', primary_key=True)
    is_enterprise = models.CharField(max_length=1)
    class Meta:
        managed = False
        db_table = 'investors'

class Legals(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    user_login = models.ForeignKey('Users', db_column='user_login', unique=True)
    class Meta:
        managed = False
        db_table = 'legals'

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

class News(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=4000)
    media = models.CharField(max_length=250)
    taken_from = models.CharField(max_length=50)
    created_at = models.DateField()
    class Meta:
        managed = False
        db_table = 'news'

class Offerants(models.Model):
    user_login = models.ForeignKey(Actives, db_column='user_login', primary_key=True)
    type = models.BigIntegerField()
    class Meta:
        managed = False
        db_table = 'offerants'

class Passives(models.Model):
    register = models.CharField(primary_key=True, max_length=20)
    user_login = models.ForeignKey('Users', db_column='user_login', unique=True)
    class Meta:
        managed = False
        db_table = 'passives'

class Passwords(models.Model):
    user_login = models.ForeignKey('Users', db_column='user_login', primary_key=True)
    password = models.CharField(max_length=20)
    question = models.CharField(max_length=20)
    answer = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'passwords'

class Payments(models.Model):
    user_login = models.ForeignKey(Actives, db_column='user_login', primary_key=True)
    money = models.FloatField()
    class Meta:
        managed = False
        db_table = 'payments'

class Professionals(models.Model):
    user_login = models.ForeignKey(Actives, db_column='user_login', primary_key=True)
    resume_pdf = models.CharField(max_length=50)
    current_job = models.CharField(max_length=20)
    current_org = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'professionals'

class Profiles(models.Model):
    user_login = models.ForeignKey(Actives, db_column='user_login', primary_key=True)
    status = models.CharField(max_length=100)
    biography = models.CharField(max_length=4000)
    avatar = models.CharField(max_length=50)
    currency = models.BigIntegerField()
    age = models.BigIntegerField()
    last_active = models.DateField()
    class Meta:
        managed = False
        db_table = 'profiles'

class Rents(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    function = models.BigIntegerField()
    length = models.BigIntegerField()
    type = models.BigIntegerField()
    offerant_login = models.ForeignKey(Offerants, db_column='offerant_login')
    class Meta:
        managed = False
        db_table = 'rents'

class Solicitudes(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    type = models.BigIntegerField()
    amount = models.FloatField()
    created_at = models.DateField()
    total = models.FloatField()
    min_price = models.FloatField()
    bought = models.CharField(max_length=1)
    value = models.ForeignKey('Vals')
    active_login = models.ForeignKey(Actives, db_column='active_login')
    passive_login = models.ForeignKey(Passives, db_column='passive_login')
    class Meta:
        managed = False
        db_table = 'solicitudes'

class Transactions(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    created_at = models.DateField()
    passive_login = models.ForeignKey(Passives, db_column='passive_login')
    active_login = models.ForeignKey(Actives, db_column='active_login')
    solved_request = models.ForeignKey(Solicitudes)
    sold_request = models.ForeignKey(Solicitudes)
    class Meta:
        managed = False
        db_table = 'transactions'

class Users(models.Model):
    login = models.CharField(primary_key=True, max_length=20)
    id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    class Meta:
        managed = False
        db_table = 'users'

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

