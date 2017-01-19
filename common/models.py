# -*-coding: utf8-*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ContactMessage(models.Model):
    name = models.CharField(
        verbose_name=_('Имя'),
        max_length=50,
    )
    email = models.EmailField(
        verbose_name=_('Email'),
    )
    message = models.TextField(
        verbose_name=_('Сообщение'),
    )

    class Meta:
        verbose_name = _('Контактное сообщение')
        verbose_name = _('Контактные сообщения')

    def __unicode__(self):
        return '{} - {}'.format(self.name, self.email)
