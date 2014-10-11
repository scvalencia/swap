# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
            ],
            options={
                'unique_together': set([('user_login', 'contact_link')]),
                'db_table': 'contacts',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
            ],
            options={
                'db_table': 'locations',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Professional',
            fields=[
            ],
            options={
                'db_table': 'professionals',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
            ],
            options={
                'db_table': 'profiles',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
