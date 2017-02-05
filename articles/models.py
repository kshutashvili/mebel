 # -*-coding: utf8-*-

from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Article(models.Model):
    SCORE_CHOICES = tuple([(x, x) for x in range(0, 6)])

    title = models.CharField(verbose_name='Название', max_length=200)
    description = RichTextField(verbose_name='Описание')
    text = RichTextField(verbose_name='Основной текст')

    creation_date = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    score = models.SmallIntegerField(
        verbose_name='Рейтинг',
        choices=SCORE_CHOICES,
        default=1
    )
    class Meta:
        verbose_name = u'Статья'
        verbose_name_plural = u'Статьи'
        ordering = ['-creation_date']