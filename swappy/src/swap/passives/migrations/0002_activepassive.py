# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passives', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivePassive',
            fields=[
            ],
            options={
                'db_table': 'activespassives',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
