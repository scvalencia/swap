# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
            ],
            options={
                'db_table': 'portfolios',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PortfolioVal',
            fields=[
            ],
            options={
                'db_table': 'portfolios',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
