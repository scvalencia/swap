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

class ActiveDump(object):

	def __init__(self, user_login, available_money):
		self.user_login = user_login
		self.available_money = available_money

	def create_object(self, login, money):
		active_object = Active(user_login = login, available_money = money)
		active_object.save()

	def __str__(self):
		ans = '('
		ans += self.user_login + ', '
		ans += str(self.available_money) + ')'
		return ans
