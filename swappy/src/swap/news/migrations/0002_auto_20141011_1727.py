# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='News',
        ),
        migrations.CreateModel(
            name='New',
            fields=[
            ],
            options={
                'db_table': 'news',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
