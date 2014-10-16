# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_campaignprofile_faction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignprofile',
            name='faction',
            field=models.ForeignKey(blank=True, to='armies.Faction', null=True),
        ),
    ]
