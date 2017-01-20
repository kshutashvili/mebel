#-*-coding:utf8-*-

from oscar.apps.order.abstract_models import AbstractOrder
from django.db import models


class SimpleOrder(models.Model):
    basket = models.ForeignKey(
        'basket.Basket', verbose_name= u'Корзина',
        null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    comment = models.TextField(blank=True, null=True)

    country = models.CharField(max_length=50, verbose_name=u'Страна')
    region = models.CharField(max_length=50, verbose_name=u'Регион')
    city = models.CharField(max_length=50, verbose_name=u'Город')
    address = models.CharField(max_length=100, verbose_name=u'Адрес')
    pass

from oscar.apps.order.models import *  # noqa


