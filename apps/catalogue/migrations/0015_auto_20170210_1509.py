# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-10 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0014_auto_20170210_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_type',
            field=models.IntegerField(blank=True, choices=[(1, '\u0424\u0438\u043a\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u0430\u044f \u0441\u043a\u0438\u0434\u043a\u0430'), (2, '\u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u0441\u043a\u0438\u0434\u043a\u0438')], null=True, verbose_name='\u0422\u0438\u043f \u0441\u043a\u0438\u0434\u043a\u0438'),
        ),
    ]