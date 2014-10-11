# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
            ],
            options={
                'unique_together': set([('follower_login', 'following_login')]),
                'db_table': 'follows',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
            ],
            options={
                'db_table': 'investors',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
