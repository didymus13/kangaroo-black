# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaigns', '0002_auto_20140909_0726'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cp', models.IntegerField(default=0)),
                ('vp', models.IntegerField(default=0)),
                ('win', models.IntegerField(default=0)),
                ('tie', models.IntegerField(default=0)),
                ('loss', models.IntegerField(default=0)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-cp', '-vp'],
            },
            bases=(models.Model,),
        ),
    ]
