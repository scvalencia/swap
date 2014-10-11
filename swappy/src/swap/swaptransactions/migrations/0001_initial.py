# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SwapTransaction',
            fields=[
            ],
            options={
                'db_table': 'swap_transactions',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
