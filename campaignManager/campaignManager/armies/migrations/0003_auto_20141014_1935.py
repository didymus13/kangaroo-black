# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('armies', '0002_auto_20140909_0726'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faction',
            options={'ordering': ['game', 'name']},
        ),
        migrations.AlterField(
            model_name='faction',
            name='name_short',
            field=models.CharField(max_length=5),
        ),
    ]
