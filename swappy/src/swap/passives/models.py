from django.db import models

from genericusers.models import GenericUser


class Passive(models.Model):
    passive_register = models.CharField(max_length=20, primary_key=True)
    user_login = models.ForeignKey(GenericUser, related_name='Passive.user_login')

    class Meta:
        db_table = 'passives'
        managed = False