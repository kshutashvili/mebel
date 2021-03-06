# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-07 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when_created', models.DateTimeField(auto_now_add=True, verbose_name='\u041a\u043e\u0433\u0434\u0430 \u0441\u043e\u0437\u0434\u0430\u043d')),
                ('image', models.ImageField(upload_to='banners', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('link', models.CharField(max_length=255, verbose_name='C\u0441\u044b\u043b\u043a\u0430')),
                ('display', models.BooleanField(default=True, verbose_name='\u041e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0442\u044c?')),
                ('position', models.BooleanField(choices=[(True, '\u0412 \u043b\u0435\u0432\u043e\u043c \u0431\u043b\u043e\u043a\u0435'), (False, '\u0412 \u0446\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u043c \u0431\u043b\u043e\u043a\u0435')], verbose_name='\u041f\u043e\u0437\u0438\u0446\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u0411\u0430\u043d\u043d\u0435\u0440',
                'verbose_name_plural': '\u0411\u0430\u043d\u043d\u0435\u0440\u044b',
            },
        ),
    ]
