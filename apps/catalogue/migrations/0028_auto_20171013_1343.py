# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-10-13 13:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0027_auto_20171013_1338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='services',
            old_name='relevant',
            new_name='is_relevant',
        ),
    ]