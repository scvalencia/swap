from django.db import models

from actives.models import Active


class Investor(models.Model):
    user_login = models.ForeignKey(Active, primary_key=True, related_name='Investor.user_login')
    is_enterprise = models.CharField(max_length=1)

    class Meta:
        db_table = 'investors'
        managed = False


class Follow(models.Model):
    follower_login = models.ForeignKey(Investor, related_name='Follow.follower_login')
    following_login = models.ForeignKey(Active, related_name='Follow.following_login')

    class Meta:
        unique_together = ('follower_login', 'following_login')
        db_table = 'follows'
        managed = False