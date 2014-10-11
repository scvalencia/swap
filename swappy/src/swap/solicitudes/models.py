from django.db import models

from actives.models import Active


class Solicitude(models.Model):
    pk_id = models.IntegerField(primary_key=True)
    request_type = models.CharField(max_length=1)
    amount = models.FloatField()
    amount_unit = models.CharField(max_length=1)
    created_at = models.DateTimeField()
    active_login = models.ForeignKey(Active, related_name='Solicitude.active_login')

    class Meta:
    	db_table = 'solicitudes'
    	managed = False