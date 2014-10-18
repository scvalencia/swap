from django.db import models

from actives.models import Active


class Investor(models.Model):
    """
    This class represents the object conversion from the 
    investors relation presented in the Oracle database.
    """
    user_login = models.ForeignKey(Active, primary_key=True, related_name='Investor.user_login', db_column='user_login')
    is_enterprise = models.CharField(max_length=1)

    class Meta:
        db_table = 'investors'
        managed = False

class InvestorDump(object):

    def __init__(self, user_login, is_enterprise):
        self.user_login = user_login
        self.is_enterprise = is_enterprise

    def __str__(self):
        ans = '('
        ans += str(self.user_login) + ', '
        ans += str(self.is_enterprise)
        ans += ')'
        return ans