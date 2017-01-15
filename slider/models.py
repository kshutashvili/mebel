# -*-coding: utf8-*-
from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class SliderSlide(models.Model):
    image = models.ImageField(verbose_name=u'Изображение', upload_to='slider')
    text = RichTextField(verbose_name=u'Текст')
    link = models.CharField(verbose_name=u'Ссылка', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = u'Слайд'
        verbose_name_plural = 'Слайды'