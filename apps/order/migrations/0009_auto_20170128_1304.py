# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-28 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_simpleorder_check_blank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simpleorder',
            name='check_blank',
            field=models.FileField(blank=True, null=True, upload_to=b'check_blanks'),
        ),
    ]
