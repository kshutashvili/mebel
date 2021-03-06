# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-09-04 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(help_text='PNG/JPG', upload_to=b'', verbose_name='\u0424\u043e\u0442\u043e')),
                ('description', models.CharField(max_length=128, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('pdf', models.FileField(help_text='PDF', upload_to=b'', verbose_name='PDF \u0444\u0430\u0439\u043b')),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u041a\u0430\u0442\u0430\u043b\u043e\u0433',
                'verbose_name_plural': '\u041a\u0430\u0442\u0430\u043b\u043e\u0433\u0438',
            },
        ),
        migrations.CreateModel(
            name='Popular',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(help_text='PNG/JPG', upload_to=b'', verbose_name='\u0424\u043e\u0442\u043e')),
                ('description', models.CharField(max_length=128, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('pdf', models.FileField(help_text='PDF', upload_to=b'', verbose_name='PDF \u0444\u0430\u0439\u043b')),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u041f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u044b\u0439 \u043a\u0430\u0442\u0430\u043b\u043e\u0433',
                'verbose_name_plural': '\u041f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u044b\u0435 \u043a\u0430\u0442\u0430\u043b\u043e\u0433\u0438',
            },
        ),
    ]
