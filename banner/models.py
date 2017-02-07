# -*-coding:utf8-*-

from __future__ import unicode_literals

from django.db import models


class Banner(models.Model):
    POSITON_CHOICES = (
        (1, u'В левом блоке'),
        (2, u'В центральном блоке')
    )
    when_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'Когда создан'
    )

    image = models.ImageField(
        upload_to='banners',
        verbose_name=u'Изображение'
    )

    link = models.CharField(
        verbose_name='Cсылка',
        max_length=255
    )

    display = models.BooleanField(
        verbose_name=u'Отображать?',
        default = True
    )

    position = models.IntegerField(
        verbose_name=u'Позиция',
        choices=POSITON_CHOICES
    )

    class Meta:
        verbose_name = u'Баннер'
        verbose_name_plural = u'Баннеры'