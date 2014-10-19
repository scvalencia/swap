from django.db import models

from solicitudes.models import Solicitude


class SwapTransaction(models.Model):
    """
    This class represents the object conversion from the 
    swap transactions relation presented in the Oracle database.
    """
    pk_id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    solicitude_1_pk = models.ForeignKey(Solicitude, related_name='SwapTransaction.solicitude_1_pk', db_column='solicitude_1_pk')
    solicitude_2_pk = models.ForeignKey(Solicitude, related_name='SwapTransaction.solicitude_2_pk', db_column='solicitude_2_pk')

    class Meta:
        db_table = 'swap_transactions'
        managed = False

class SwapTransactionDump(object):

    def __init__(self, pk_id, created_at, solicitude_1_pk, solicitude_2_pk):
        self.pk_id = pk_id
        self.created_at = created_at
        self.solicitude_1_pk = solicitude_1_pk
        self.solicitude_2_pk = solicitude_2_pk

    def __str__(self):
        ans = '('
        ans += str(self.pk_id) + ', '
        ans += str(self.created_at) + ', '
        ans += str(self.solicitude_1_pk) + ', '
        ans += str(self.solicitude_2_pk)
        ans += ')'
        return ans