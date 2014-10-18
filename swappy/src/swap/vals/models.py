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
    offerant_login = models.ForeignKey(Offerant, related_name='Rent.offerant_login', db_column='offerant_login')

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
    rent_id = models.ForeignKey(Rent, related_name='Val.rent_id', db_column='rent_id')

    class Meta:
        db_table = 'vals'
        managed = False

class RentDump(object):

    def __init__(self, pk_id, rent_name, desc, rent_function, rent_len, rent_tp, login):
        self.pk_id = pk_id
        self.rent_name = rent_name
        self.description = desc
        self.rent_function = rent_function
        self.rent_length = rent_len
        self.rent_type = rent_tp
        self.offerant_login = login

    def __str__(self):
        ans = '('
        ans += str(self.pk_id) + ', '
        ans += str(self.rent_name) + ', '
        ans += str(self.description) + ', '
        ans += str(self.rent_function) + ', '
        ans += str(self.rent_length) + ', '
        ans += str(self.rent_type) + ', '
        ans += str(self.offerant_login)
        ans += ')'
        return ans

class ValDump(object):

    def __init__(self, pk, name, desc, val_type, amount, price, rent_id):
        self.pk_id = pk
        self.val_name = name
        self.description = desc
        self.val_type = val_type
        self.amount = amount
        self.price = price
        self.rent_id = rent_id

    def __str__(self):
        ans = '('
        ans += str(self.pk_id) + ', '
        ans += str(self.val_name) + ', '
        ans += str(self.description) + ', '
        ans += str(self.val_type) + ', '
        ans += str(self.amount) + ', '
        ans += str(self.price) + ', '
        ans += str(self.rent_id)
        ans += ')'
        return ans