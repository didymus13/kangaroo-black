# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_auto_20140909_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='looking_for_players',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, b'setting up'), (300, b'playing'), (500, b'finished'), (600, b'on hiatus')]),
            preserve_default=True,
        ),
    ]
