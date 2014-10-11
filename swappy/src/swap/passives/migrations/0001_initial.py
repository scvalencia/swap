# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Passive',
            fields=[
            ],
            options={
                'db_table': 'passives',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
