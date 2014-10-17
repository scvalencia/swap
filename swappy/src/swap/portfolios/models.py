from django.db import models

from genericusers.models import GenericUser
from vals.models import Val


class Portfolio(models.Model):
    """
    This class represents the object conversion from the 
    portfolio relation presented in the Oracle database.
    """
    pk_id = models.IntegerField(primary_key=True)
    user_login = models.ForeignKey(GenericUser, related_name='Portfolio.user_login')
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
    pk_portfolio = models.ForeignKey(Portfolio, related_name='PortfolioVal.pk_portfolio')
    pk_val = models.ForeignKey(Val, related_name='PortfolioVal.pk_val')

    class Meta:
        db_table = 'portfolios'
        managed = False