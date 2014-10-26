# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0006_turn_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='map',
            field=models.ImageField(null=True, upload_to=b'photos/%Y/%m/%d', blank=True),
            preserve_default=True,
        ),
    ]
