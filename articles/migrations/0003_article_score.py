# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-24 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20170117_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='score',
            field=models.SmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433'),
        ),
    ]
