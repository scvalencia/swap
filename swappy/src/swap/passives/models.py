from django.db import models

from actives.models import Active
from genericusers.models import GenericUser


class Passive(models.Model):
    """
    This class represents the object conversion from the 
    passives relation presented in the Oracle database.
    """
    passive_register = models.CharField(max_length=20, primary_key=True)
    user_login = models.ForeignKey(GenericUser, related_name='Passive.user_login', db_column='user_login')

    class Meta:
        db_table = 'passives'
        managed = False


class ActivePassive(models.Model):
    """
    This class represents the object conversion from the 
    passives relation presented in the Oracle database.
    """
    active_login = models.ForeignKey(Active, related_name='ActivePassive.active_login', db_column='active_login')
    passive_login = models.ForeignKey(Passive, related_name='ActivePassive.passive_register', db_column='passive_register')

    class Meta:
        db_table = 'activespassives'
        managed = False