# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20141117_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='live_date',
            field=models.DateField(default=datetime.datetime(2014, 11, 21, 13, 29, 6, 357575)),
            preserve_default=True,
        ),
    ]
