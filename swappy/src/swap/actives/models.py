from django.db import models

from genericusers.models import GenericUser


class Active(models.Model):
    """
    This class represents the object conversion from the 
    actives relation presented in the Oracle database.
    """
    user_login = models.ForeignKey(GenericUser, primary_key=True, related_name='Active.user_login',  db_column='user_login')
    available_money = models.FloatField()

    class Meta:
        db_table = 'actives'
        managed = False

class ActiveDump(object):

	def __init__(self, user_login, passive_register, available_money):
		self.user_login = user_login
		self.passive_register = passive_register
		self.available_money = available_money

	def create_object(self, login, reg, money):
		pass
