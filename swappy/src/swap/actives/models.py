from django.db import models

from genericusers.models import GenericUser


class Active(models.Model):
    """
    This class represents the object conversion from the 
    actives relation presented in the Oracle database.
    """
    user_login = models.ForeignKey(GenericUser, primary_key=True, related_name='Active.user_login')
    available_money = models.FloatField()

    class Meta:
        db_table = 'actives'
        managed = False