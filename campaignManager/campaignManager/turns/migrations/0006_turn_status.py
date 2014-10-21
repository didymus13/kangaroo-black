# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0005_auto_20140930_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='status',
            field=models.PositiveIntegerField(default=0, choices=[[0, b'initial'], [50, b'active'], [100, b'complete']]),
            preserve_default=True,
        ),
    ]
