# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20141115_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='test-post', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='live_date',
            field=models.DateField(default=datetime.datetime(2014, 11, 17, 8, 12, 48, 205541)),
            preserve_default=True,
        ),
    ]
