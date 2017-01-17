# -*-coding: utf8-*-

from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Article(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    description = RichTextField(verbose_name='Описание')
    text = RichTextField(verbose_name='Основной текст')
    creation_date = models.DateField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = u'Статья'
        verbose_name_plural = u'Статьи'
        ordering = ['-creation_date']