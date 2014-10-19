from django.db import models

from actives.models import Active


class Solicitude(models.Model):
    """
    This class represents the object conversion from the 
    solicitudes relation presented in the Oracle database.
    """
    pk_id = models.IntegerField(primary_key=True)
    request_type = models.CharField(max_length=1)
    amount = models.FloatField()
    amount_unit = models.CharField(max_length=1)
    created_at = models.DateTimeField()
    active_login = models.ForeignKey(Active, related_name='Solicitude.active_login', db_column='active_login')

    class Meta:
        db_table = 'solicitudes'
        managed = False

class SolicitudeDump(object):

    def __init__(self, pk_id, request_type, amount, amount_unit, created_at, active_login):
        self.pk_id = pk_id
        self.request_type = request_type
        self.amount = amount
        self.amount_unit = amount_unit
        self.created_at = created_at
        self.active_login = active_login

    def __str__(self):
        ans = '('
        ans += str(self.pk_id) + ', '
        ans += str(self.request_type) + ', '
        ans += str(self.amount) + ', '
        ans += str(self.amount_unit) + ', '
        ans += str(self.created_at) + ', '
        ans += str(self.active_login)
        ans+= ')'
        return ans