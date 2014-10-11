# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
            ],
            options={
                'db_table': 'rents',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Val',
            fields=[
            ],
            options={
                'db_table': 'vals',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
