# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0004_challenge_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='challenge',
            options={'ordering': ['-issued_date', '-turn']},
        ),
        migrations.AlterField(
            model_name='challenge',
            name='status',
            field=models.PositiveIntegerField(default=0, choices=[[0, b'pending'], [10, b'accepted'], [100, b'complete']]),
        ),
    ]
