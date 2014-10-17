from django.db import models

from actives.models import Active
from offerants.models import Offerant


class Rent(models.Model):
    """
    This class represents the object conversion from the 
    rents relation presented in the Oracle database.
    """
    pk_id = models.IntegerField(primary_key=True)
    rent_name = models.CharField(max_length=20)
    description = models.CharField(max_length=140)
    rent_function = models.CharField(max_length=1)
    rent_length = models.CharField(max_length=1)
    rent_type = models.CharField(max_length=1)
    offerant_login = models.ForeignKey(Offerant, related_name='Rent.offerant_login')

    class Meta:
        db_table='rents'
        managed = False


class Val(models.Model):
    """
    This class represents the object conversion from the 
    vals relation presented in the Oracle database.
    """
    pk_id = models.IntegerField(primary_key=True)
    val_name = models.CharField(max_length=20)
    description = models.CharField(max_length=140)
    val_type = models.CharField(max_length=1)
    amount = models.IntegerField()
    price = models.FloatField()
    rent_id = models.ForeignKey(Rent, related_name='Val.rent_id')

    class Meta:
        db_table = 'vals'
        managed = False