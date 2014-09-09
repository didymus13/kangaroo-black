# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_auto_20140909_0726'),
        ('armies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='army',
            name='faction',
        ),
        migrations.RemoveField(
            model_name='army',
            name='user',
        ),
        migrations.DeleteModel(
            name='Army',
        ),
    ]
