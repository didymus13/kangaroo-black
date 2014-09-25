# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0002_challenge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='recipient',
            field=models.ForeignKey(related_name=b'recipient', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
