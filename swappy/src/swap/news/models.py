from django.db import models

from actives.models import Active


class New(models.Model):
    pk_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    taken_from = models.CharField(max_length=50)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'news'
        managed = False


class Comment(models.Model):
    pk_id = models.IntegerField(primary_key=True)
    comment_content = models.CharField(max_length=140)
    created_at = models.DateTimeField()
    news_pk = models.ForeignKey(New, related_name='Comment.news_pk')
    user_login = models.ForeignKey(Active, related_name='Comment.user_login')

    class Meta:
        db_table = 'comments'
        managed = False