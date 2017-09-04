# -*-coding: utf8-*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from pyPdf import PdfFileReader
from django.core.exceptions import ValidationError
from utils import get_admin_thumb


class CatalogAbstract(models.Model):
    class Meta:
        abstract = True

    photo = models.ImageField(
        verbose_name=_('Фото'),
        help_text=_('PNG/JPG'),
    )
    description = models.CharField(
        max_length=128,
        verbose_name=_('Краткое описание'),
    )
    pdf = models.FileField(
        verbose_name=_('PDF файл'),
        help_text=_('PDF'),
    )
    creation_date = models.DateField(
        verbose_name=_('Дата создания'),
        auto_now_add=True
    )

    def clean(self, *args, **kwargs):
        try:
            PdfFileReader(self.pdf)
        except Exception as e:
            raise ValidationError(_('Разрешен только PDF файл'))

    def admin_photo(self):
        return get_admin_thumb(self.photo, '128x128')

    admin_photo.allow_tags = True
    admin_photo.short_description = _('Фото каталога')

    def __unicode__(self):
        return self.description


class Catalog(CatalogAbstract):
    class Meta:
        verbose_name = _('Каталог')
        verbose_name_plural = _('Каталоги')


class Popular(CatalogAbstract):
    class Meta:
        verbose_name = _('Популярный каталог')
        verbose_name_plural = _('Популярные каталоги')
