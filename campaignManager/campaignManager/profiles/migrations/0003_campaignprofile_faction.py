# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('armies', '0002_auto_20140909_0726'),
        ('profiles', '0002_campaignprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignprofile',
            name='faction',
            field=models.ForeignKey(default=1, to='armies.Faction'),
            preserve_default=False,
        ),
    ]
