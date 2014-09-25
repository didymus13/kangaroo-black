# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('turns', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(max_length=254)),
                ('issued_date', models.DateTimeField(auto_now_add=True)),
                ('challenger', models.ForeignKey(related_name=b'challenger', to=settings.AUTH_USER_MODEL)),
                ('recipient', models.ForeignKey(related_name=b'recipient', to=settings.AUTH_USER_MODEL)),
                ('turn', models.ForeignKey(to='turns.Turn')),
                ('winner', models.ForeignKey(related_name=b'winner', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-turn', '-issued_date'],
            },
            bases=(models.Model,),
        ),
    ]
