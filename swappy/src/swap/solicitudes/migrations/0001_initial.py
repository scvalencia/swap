# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitude',
            fields=[
            ],
            options={
                'db_table': 'solicitudes',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
