#-*-coding:utf8-*-

from django.db import models
from django.core.files.base import ContentFile
from django.template.loader import get_template
from django.conf import settings
from django.contrib.sites.models import Site

import pdfkit


class SimpleOrder(models.Model):
    STATUS_CHOICES =(
        (1, u'Отменен'),
        (2, u'В стадии обработки'),
        (3, u'На производстве'),
        (4, u'Огружен'),
        (5, u'Выполнен'),
    )

    when_created = models.DateTimeField(
        verbose_name=u'Время создания',
        auto_now_add=True,
    )
    basket = models.ForeignKey(
        'basket.Basket',
        verbose_name= u'Корзина',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    order_status = models.IntegerField(
        verbose_name=u'Статус',
        choices=STATUS_CHOICES,
        default=2
    )

    name = models.CharField(
        max_length=50,
        verbose_name=u'Имя'
    )
    phone = models.CharField(
        max_length=12,
        verbose_name=u'Телефон'
    )
    comment = models.TextField(blank=True, null=True, verbose_name=u'Коментарий')

    email = models.EmailField(
        max_length=50,
        verbose_name=u'E-mail'
    )
    region = models.CharField(
        max_length=50,
        verbose_name=u'Регион'
    )
    city = models.ForeignKey(
        'ShippingCity',
        verbose_name=u'Город'
    )
    address = models.CharField(
        max_length=100,
        verbose_name=u'Адрес'
    )

    check_blank = models.FileField(
        verbose_name=u'Чек',
        upload_to='orders/check_blanks/%Y/%m/%d',
        null=True,
        blank=True
    )

    manufacture_blank = models.FileField(
        verbose_name=u'Бланк производства',
        upload_to='orders/manufature_blanks/%Y/%m/%d',
        null=True,
        blank=True
    )

    shipping_blank =models.FileField(
        verbose_name=u'Бланк доставки',
        upload_to='orders/shipping_blanks/%Y/%m/%d',
        null=True,
        blank=True
    )

    order_price = models.CharField(
        max_length=12,
        default='0.0',
        verbose_name=u'Сумма заказа',
        blank=True,
    )

    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'

    def __unicode__(self):
        return '%s %s' %(self.when_created, self.order_status)

    def create_pdf(self, template_name, add_ctx={}):
        ctx = {'order': self, 'site': Site.objects.get_current()}
        if add_ctx:
            ctx.update(add_ctx)
        tmplt = get_template(template_name).render(ctx)
        config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_CMD)
        output_file = pdfkit.from_string(tmplt, False, configuration=config)
        return output_file

    def create_check_blank(self):
        output_file = self.create_pdf('pdf/check_blank.html')
        if output_file:
            output_filname = 'order_check__%s.pdf' % (self.basket.id)
            self.check_blank.save(output_filname, ContentFile(output_file))

    def create_manufacture_blank(self):
        output_file = self.create_pdf('pdf/manufacture_blank.html')
        output_filname = 'manufacture_blank__%s.pdf' % (self.basket.id)
        if output_file:
            self.manufacture_blank.save(output_filname, ContentFile(output_file))

    def create_shipping_blank(self):
        output_file = self.create_pdf('pdf/shipping_blank.html')
        output_filname = 'shipping_blank__%s.pdf' % (self.basket.id)
        if output_file:
            self.shipping_blank.save(output_filname, ContentFile(output_file))

    def save(self, *args, **kwargs):
        super(SimpleOrder, self).save(*args, **kwargs)
        self.order_price = self.total_price
        if not self.check_blank:
            self.create_check_blank()
        if not self.manufacture_blank:
            self.create_manufacture_blank()
        if not self.shipping_blank:
            self.create_shipping_blank()


    @property
    def shipping_price(self):
        return self.city.shipping_price

    @property
    def total_price(self):
        if self.basket.is_tax_known:
            return self.basket.total_incl_tax+self.shipping_price
        else:
            return self.basket.total_excl_tax+self.shipping_price

    def __unicode__(self):
        return '%s %s %s'%(self.name, self.phone, self.email)


class ShippingCity(models.Model):
    name = models.CharField(
        verbose_name=u'Город',
        max_length=100
    )

    shipping_price = models.DecimalField(
        verbose_name=u'Стоимость доставки',
        default=0.00,
        decimal_places=2,
        max_digits=12
    )

    class Meta:
        verbose_name = u'Город доставки'
        verbose_name_plural = u'Города доставки'

    def __unicode__(self):
        return u'%s'%(self.name)


class OneClickOrder(models.Model):
    when_created = models.DateTimeField(
        verbose_name=u'Когда создан',
        auto_now_add=True
    )

    product = models.ForeignKey(
        'catalogue.Product',
        verbose_name='Товар',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    phone = models.CharField(
        max_length=12,
        verbose_name=u'Телефон'
    )

from oscar.apps.order.models import *  # noqa
