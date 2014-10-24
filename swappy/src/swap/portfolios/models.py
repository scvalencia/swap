from django.db import models

from genericusers.models import GenericUser
from vals.models import Val


class Portfolio(models.Model):
    """
    This class represents the object conversion from the 
    portfolio relation presented in the Oracle database.
    """
    pk_id = models.IntegerField(primary_key=True)
    user_login = models.ForeignKey(GenericUser, related_name='Portfolio.user_login', db_column='user_login')
    risk = models.CharField(max_length=1)

    class Meta:
        db_table = 'portfolios'
        managed = False

class PortfolioVal(models.Model):
    """
    This class represents the object conversion from the 
    portfolio relation presented in the Oracle database.
    """
    pk_id = models.IntegerField(primary_key=True)
    pk_portfolio = models.ForeignKey(Portfolio, related_name='PortfolioVal.pk_portfolio', db_column='pk_portfolio')
    pk_val = models.ForeignKey(Val, related_name='PortfolioVal.pk_val', db_column='pk_val')

    class Meta:
        db_table = 'portfolios'
        managed = False

class PortfolioDump(object):

    def __init__(self, user_login, risk, pk_id):
        self.pk_id = pk_id
        self.user_login = user_login
        self.risk = risk

    def __str__(self):
        ans = '('
        ans += str(self.pk_id) + ', '
        ans += str(self.user_login) + ', '
        ans += str(self.risk)
        ans += ')'
        return ans