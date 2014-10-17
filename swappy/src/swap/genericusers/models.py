from django.db import models


class GenericUser(models.Model):
    """
    This class represents the object conversion from the 
    users relation presented in the Oracle database.
    """
    login = models.CharField(max_length=20, primary_key=True)
    user_id = models.CharField(max_length=20)
    user_pass = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    class Meta:
        db_table = 'users'
        managed = False


class Legal(models.Model):
    """
    This class represents the object conversion from the 
    users relation presented in the Oracle database.
    """
    legal_id = models.CharField(max_length=20, primary_key=True)
    legal_name = models.CharField(max_length=20)
    user_login = models.ForeignKey(GenericUser, related_name='Legal.user_login', db_column='user_login')

    class Meta:
        db_table = 'legals'
        managed = False