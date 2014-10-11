from django.db import models


class GenericUser(models.Model):
    login = models.CharField(max_length=20, primary_key=True)
    user_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    class Meta:
        db_table = 'users'
        managed = False


class Legal(models.Model):
    legal_id = models.CharField(max_length=20, primary_key=True)
    legal_name = models.CharField(max_length=20)
    user_login = models.ForeignKey(GenericUser, related_name='Legal.user_login')

    class Meta:
        db_table = 'legals'
        managed = False


class Password(models.Model):
    user_login = models.ForeignKey(GenericUser, primary_key=True, related_name='Password.user_login')
    user_password = models.CharField(max_length=20)
    question = models.CharField(max_length=20)
    answer = models.CharField(max_length=20)

    class Meta:
        db_table = 'passwords'
        managed = False