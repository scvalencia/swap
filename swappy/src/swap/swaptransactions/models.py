from django.db import models

from solicitudes.models import Solicitude


class SwapTransaction(models.Model):
    pk_id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    solicitude_1_pk = models.ForeignKey(Solicitude, related_name='SwapTransaction.solicitude_1_pk')
    solicitude_2_pk = models.ForeignKey(Solicitude, related_name='SwapTransaction.solicitude_2_pk')

    class Meta:
        db_table = 'swap_transactions'
        managed = False