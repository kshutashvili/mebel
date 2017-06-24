 # -*-coding: utf8-*-

from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Article(models.Model):
    SCORE_CHOICES = tuple([(x, x) for x in range(0, 6)])

    title = models.CharField(verbose_name='Название', max_length=200)
    title_tag = models.CharField(
        verbose_name=u'HTML-тег Title',
        max_length=255,
        blank=True,
        null=True
    )

    meta_description = models.CharField(
        verbose_name=u'Мета-тег Description',
        max_length=255,
        blank=True,
        null=True
    )
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