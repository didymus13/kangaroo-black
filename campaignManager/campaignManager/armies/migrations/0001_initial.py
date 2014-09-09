# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Army',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('photo', models.ImageField(null=True, upload_to=b'photos/%Y/%m/%d', blank=True)),
                ('blurb', models.TextField(blank=True)),
                ('armylist', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'armies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('photo', models.ImageField(null=True, upload_to=b'photos/%Y/%m/%d', blank=True)),
                ('slug', models.SlugField(null=True)),
                ('name_short', models.CharField(max_length=4)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('photo', models.ImageField(null=True, upload_to=b'photos/%Y/%m/%d', blank=True)),
                ('slug', models.SlugField(null=True)),
                ('name_short', models.CharField(max_length=5)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='faction',
            name='game',
            field=models.ForeignKey(to='armies.Game'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='army',
            name='faction',
            field=models.ForeignKey(blank=True, to='armies.Faction', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='army',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
