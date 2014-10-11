from django.db import models

from genericusers.models import GenericUser
from passives.models import Passive


class Active(models.Model):
    user_login = models.ForeignKey(GenericUser, primary_key=True, related_name='Active.user_login')
    passive_register = models.ForeignKey(Passive, related_name='Active.passive_register')
    available_money = models.FloatField()

    class Meta:
        db_table = 'actives'
        managed = False