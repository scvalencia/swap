from django.db import models

from actives.models import Active


class Offerant(models.Model):
    """
    This class represents the object conversion from the 
    offerants relation presented in the Oracle database.
    """
    user_login = models.ForeignKey(Active, primary_key=True, related_name='Offerant.user_login')
    offerant_type = models.CharField(max_length=1)

    class Meta:
        db_table = 'offerants'
        managed = False