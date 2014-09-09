# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaignarmy',
            name='army',
        ),
        migrations.RemoveField(
            model_name='campaignarmy',
            name='campaign',
        ),
        migrations.DeleteModel(
            name='CampaignArmy',
        ),
    ]
