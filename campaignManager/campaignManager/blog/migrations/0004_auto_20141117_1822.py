# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20141117_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='live_date',
            field=models.DateField(default=datetime.datetime(2014, 11, 17, 18, 22, 54, 868982)),
            preserve_default=True,
        ),
    ]
