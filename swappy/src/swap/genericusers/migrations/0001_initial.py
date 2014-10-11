# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GenericUser',
            fields=[
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Legal',
            fields=[
            ],
            options={
                'db_table': 'legals',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Password',
            fields=[
            ],
            options={
                'db_table': 'passwords',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
