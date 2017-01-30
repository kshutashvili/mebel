#-*-coding:utf8-*-

from django.db import models
from django.core.files.base import ContentFile
from django.template.loader import get_template
from django.conf import settings

import pdfkit


class SimpleOrder(models.Model):
    basket = models.ForeignKey(
        'basket.Basket', verbose_name= u'Корзина',
        null=True, blank=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=50, verbose_name=u'Имя')
    phone = models.CharField(max_length=12, verbose_name=u'Телефон')
    comment = models.TextField(blank=True, null=True, verbose_name=u'Коментарий')

    email = models.EmailField(max_length=50, verbose_name=u'E-mail')
    region = models.CharField(max_length=50, verbose_name=u'Регион')
    city = models.CharField(max_length=50, verbose_name=u'Город')
    address = models.CharField(max_length=100, verbose_name=u'Адрес')

    check_blank = models.FileField(upload_to='check_blanks/%Y/%m/%d', null=True, blank=True)

    def create_check_blank(self):
        tmplt = get_template('pdf/check_blank.html').render({'basket': self.basket})

        output_filname = 'order_check__%s.pdf' % (self.basket.id)

        config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_CMD)
        output_file = pdfkit.from_string(tmplt, False, configuration=config)

        if output_file:
            self.check_blank.save(output_filname, ContentFile(output_file))


from oscar.apps.order.models import *  # noqa


