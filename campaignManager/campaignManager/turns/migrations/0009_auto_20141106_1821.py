# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0008_turn_map_thumbnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='turn',
            old_name='map',
            new_name='_map',
        ),
    ]
