# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0003_auto_20140922_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='status',
            field=models.PositiveIntegerField(default=0, choices=[[b'pending', 0], [b'accepted', 10], [b'complete', 100]]),
            preserve_default=True,
        ),
    ]
