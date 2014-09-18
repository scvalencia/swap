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


class Actives(models.Model):
    user_login = models.ForeignKey('users.Users', db_column='user_login', primary_key=True, related_name='actives(models.model):_user_login')
    passive_register = models.ForeignKey('passives.Passives', db_column='passive_register', unique=True, related_name='actives(models.model):_passive_register')

    class Meta:
        managed = False
        db_table = 'actives'


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=240, blank=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey('authgroup.AuthGroup', related_name='authgrouppermissions(models.model):_group')
    permission = models.ForeignKey('authpermission.AuthPermission', related_name='authgrouppermissions(models.model):_permission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=150, blank=True)
    content_type = models.ForeignKey('djangocontenttype.DjangoContentType', related_name='authpermission(models.model):_content_type')
    codename = models.CharField(max_length=300, blank=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=384, blank=True)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=90, blank=True)
    first_name = models.CharField(max_length=90, blank=True)
    last_name = models.CharField(max_length=90, blank=True)
    email = models.CharField(max_length=225, blank=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey('authuser.AuthUser', related_name='authusergroups(models.model):_user')
    group = models.ForeignKey('authgroup.AuthGroup', related_name='authusergroups(models.model):_group')

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey('authuser.AuthUser', related_name='authuseruserpermissions(models.model):_user')
    permission = models.ForeignKey('authpermission.AuthPermission', related_name='authuseruserpermissions(models.model):_permission')

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class Comments(models.Model):
    pk_id = models.CharField(primary_key=True, max_length=100)
    content = models.CharField(max_length=4000)
    created_at = models.DateField()
    news_title = models.ForeignKey('news.News', db_column='news_title', related_name='comments(models.model):_news_title')
    news_taken_from = models.ForeignKey('news.News', db_column='news_taken_from', related_name='comments(models.model):_news_taken_from')
    user_login = models.ForeignKey('actives.Actives', db_column='user_login', related_name='comments(models.model):_user_login')

    class Meta:
        managed = False
        db_table = 'comments'


class Contacts(models.Model):
    user_login = models.ForeignKey('actives.Actives', db_column='user_login', related_name='contacts(models.model):_user_login')
    link = models.CharField(max_length=50)
    name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'contacts'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=600, blank=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True)
    content_type = models.ForeignKey('djangocontenttype.DjangoContentType', blank=True, null=True, related_name='djangoadminlog(models.model):_content_type')
    user = models.ForeignKey('authuser.AuthUser', related_name='djangoadminlog(models.model):_user')

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=300, blank=True)
    app_label = models.CharField(max_length=300, blank=True)
    model = models.CharField(max_length=300, blank=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=765, blank=True)
    name = models.CharField(max_length=765, blank=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=120)
    session_data = models.TextField(blank=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Follows(models.Model):
    follower_login = models.ForeignKey('investors.Investors', db_column='follower_login', related_name='follows(models.model):_follower_login')
    following_login = models.ForeignKey('actives.Actives', db_column='following_login', related_name='follows(models.model):_following_login')

    class Meta:
        managed = False
        db_table = 'follows'


class Investors(models.Model):
    user_login = models.ForeignKey('actives.Actives', db_column='user_login', primary_key=True, related_name='investors(models.model):_user_login')
    is_enterprise = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'investors'


class Legals(models.Model):
    pk_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    user_login = models.ForeignKey('users.Users', db_column='user_login', unique=True, related_name='legals(models.model):_user_login')

    class Meta:
        managed = False
        db_table = 'legals'


class Locations(models.Model):
    user_login = models.ForeignKey('actives.Actives', db_column='user_login', primary_key=True, related_name='locations(models.model):_user_login')
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
    user_login = models.ForeignKey('actives.Actives', db_column='user_login', primary_key=True, related_name='offerants(models.model):_user_login')
    offerant_type = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'offerants'


class Passives(models.Model):
    register = models.CharField(primary_key=True, max_length=20)
    user_login = models.ForeignKey('users.Users', db_column='user_login', unique=True, related_name='passives(models.model):_user_login')

    class Meta:
        managed = False
        db_table = 'passives'


class Passwords(models.Model):
    user_login = models.ForeignKey('users.Users', db_column='user_login', primary_key=True, related_name='passwords(models.model):_user_login')
    password = models.CharField(max_length=20)
    question = models.CharField(max_length=20)
    answer = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'passwords'


class Payments(models.Model):
    user_login = models.ForeignKey('actives.Actives', db_column='user_login', primary_key=True, related_name='payments(models.model):_user_login')
    money = models.FloatField()

    class Meta:
        managed = False
        db_table = 'payments'


class Professionals(models.Model):
    user_login = models.ForeignKey('actives.Actives', db_column='user_login', primary_key=True, related_name='professionals(models.model):_user_login')
    resume_pdf = models.CharField(max_length=50)
    current_job = models.CharField(max_length=20)
    current_org = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'professionals'


class Profiles(models.Model):
    user_login = models.ForeignKey('actives.Actives', db_column='user_login', primary_key=True, related_name='profiles(models.model):_user_login')
    status = models.CharField(max_length=100)
    biography = models.CharField(max_length=4000)
    avatar = models.CharField(max_length=50)
    currency = models.BigIntegerField()
    age = models.BigIntegerField()
    last_active = models.DateField()

    class Meta:
        managed = False
        db_table = 'profiles'


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


class Typevals(models.Model):
    pk_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    offerant_login = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'typevals'


class Users(models.Model):
    login = models.CharField(primary_key=True, max_length=20)
    pk_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'users'


class Vals(models.Model):
    pk_id = models.CharField(primary_key=True, max_length=100)
    typeval = models.ForeignKey('typevals.Typevals', related_name='vals(models.model):_typeval')
    amount = models.BigIntegerField()
    price = models.FloatField()
    active_login = models.ForeignKey('actives.Actives', db_column='active_login', related_name='vals(models.model):_active_login')
    typerent = models.ForeignKey('typerents.Typerents', related_name='vals(models.model):_typerent')

    class Meta:
        managed = False
        db_table = 'vals'

