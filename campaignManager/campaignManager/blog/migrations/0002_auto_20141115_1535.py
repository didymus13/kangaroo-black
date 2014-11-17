# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-live_date', 'title']},
        ),
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='live_date',
            field=models.DateField(default=datetime.datetime(2014, 11, 15, 15, 35, 7, 718868)),
            preserve_default=True,
        ),
    ]
