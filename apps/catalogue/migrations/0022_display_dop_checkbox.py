# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-07-20 21:22
from __future__ import unicode_literals

from django.db import migrations


def display_dop_checkbox(apps, schema_editor):
    OptionGroup = apps.get_model("catalogue", "OptionGroup")
    OptionGroup.objects.filter(code="dop").update(display_type='checkbox')


class Migration(migrations.Migration):
    dependencies = [
        ('catalogue', '0021_auto_20170720_1842'),
    ]

    operations = [
        migrations.RunPython(display_dop_checkbox)
    ]