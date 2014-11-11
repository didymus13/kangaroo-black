# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0009_auto_20141106_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turn',
            name='map_thumbnail',
        ),
    ]
