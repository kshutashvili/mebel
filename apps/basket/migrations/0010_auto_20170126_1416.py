# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-26 14:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0009_auto_20170120_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineoptionchoice',
            name='option',
        ),
        migrations.AlterField(
            model_name='lineoptionchoice',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.OptionInfo', verbose_name='\u0412\u044b\u0431\u0440\u0430\u043d\u044b\u0439 \u0432\u0430\u0440\u0438\u0430\u043d\u0442'),
        ),
    ]
