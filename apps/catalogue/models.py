# -*-coding:utf8-*-
from lxml import etree
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractCategory

from django.db import models
from django.template import Template, Context
from django.utils.translation import get_language
from django.contrib.staticfiles.finders import find
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.conf import settings

from apps.basket.models import Line
from apps.partner.models import StockRecord
import os


class Category(AbstractCategory):

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

    def get_absolute_url(self):
        """
                Our URL scheme means we have to look up the category's ancestors. As
                that is a bit more expensive, we cache the generated URL. That is
                safe even for a stale cache, as the default implementation of
                ProductCategoryView does the lookup via primary key anyway. But if
                you change that logic, you'll have to reconsider the caching
                approach.
                """
        current_locale = get_language()
        cache_key = 'CATEGORY_URL_%s_%s' % (current_locale, self.pk)
        url = cache.get(cache_key)
        if not url:
            url = reverse(
                'catalogue:category',
                kwargs={'category_slug': self.full_slug})
            cache.set(cache_key, url)
        return url

class Product(AbstractProduct):
    DISCOUNT_TYPE_CHOICES = (
        (1, u'Фиксированая скидка'),
        (2, u'Процент скидки')
    )

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

    discount_type = models.IntegerField(
        verbose_name=u'Тип скидки',
        choices=DISCOUNT_TYPE_CHOICES,
        blank=True,
        null=True
    )

    discount_value = models.DecimalField(
        verbose_name=u'Значение скидки',
        default=0.00,
        decimal_places=2,
        max_digits=12
    )

    def get_preview_info(self):
        prev_list = []
        if self.multiple_options:
            for moption in self.multiple_options.all():
                if moption.group.preview and moption.choices.all():
                    prev_list.append(
                        '%s(%s)' % (moption.choices.all()[0].variant.name,
                        ','.join([var.variant.name for var in moption.choices.all()[1:]]))
                    )
            return 'X'.join(prev_list)

        return ''

    def get_price(self):
        price = StockRecord.objects.get(product__id=self.id)
        return price.price_retail

    def get_absolute_url(self):
        """
        Overriding parent method
        Return a product's absolute url
        """
        category = self.get_categories().first()
        if category:
            category_slug = '{}'.format(category.slug)
            category_id = category.id
        else:
            category_slug = 'others'
            category_id = ''
        return reverse('catalogue:detail',
                       kwargs={'category_slug': category_slug,
                               'product_slug': self.slug, 'pk': self.id })


class MultipleOption(models.Model):
    product = models.ForeignKey(
        'Product',
        related_name='multiple_options',
        verbose_name=u'Товар'
    )

    group = models.ForeignKey(
        'OptionGroup',
        related_name='Choices',
        verbose_name=u'Група опций',
        default=1
    )

    is_required = models.BooleanField(
        verbose_name=u'Обязательное поле ?',
        default=True
    )

    class Meta:
        verbose_name = u'Множественная опция продукта'
        verbose_name_plural = u'Множественные опции продукта'

    def __unicode__(self):
        return u'%s' % self.group.name


class OptionInfo(models.Model):
    multi_option = models.ForeignKey(
        'MultipleOption',
        related_name='choices',
        verbose_name=u'Опция'
    )

    variant = models.ForeignKey(
        'OptionVariant',
        related_name='infos',
        verbose_name=u'Вариант',
    )

    additional_price = models.DecimalField(
        verbose_name=u'Наценка',
        default=0,
        decimal_places=2,
        max_digits=12,
    )

    class Meta:
        verbose_name = u'Информация опции'
        verbose_name_plural = u'Информации опций'

    def __unicode__(self):
        return '%s %s %s'%(unicode(self.multi_option), self.variant.name, self.additional_price)


class OptionGroup(models.Model):
    TYPE_CHOICES = (
        ('radio', 'radio'),
        ('select', 'select'),
        ('checkbox', 'checkbox')
    )

    name = models.CharField(max_length=100, verbose_name=u'Название групы')

    code = models.CharField(
        max_length=100,
        verbose_name=u'Код групы',
        help_text=u'Только латинские символы'
    )

    is_filter = models.BooleanField(verbose_name=u'Фильтровать?',default=True)

    display_type = models.CharField(
        choices=TYPE_CHOICES,
        default='radio',
        max_length=100,
        verbose_name=u'Тип отображения'
    )

    preview = models.BooleanField(default=False)

    postfix = models.CharField(
        max_length=5,
        blank=True, default='',
        verbose_name=u'Постфикс'
    )

    class Meta:
        verbose_name = u'Група опций'
        verbose_name_plural = u'Групы опций'

    def __unicode__(self):
        return self.name


class OptionVariant(models.Model):
    group = models.ForeignKey(
        OptionGroup,
        related_name='variants',
        verbose_name=u'Група'
    )

    name = models.CharField(
        max_length=100,
        verbose_name=u'Название'
    )

    image = models.ImageField(
        verbose_name=u'Изображение',
        upload_to='options_image',
        blank=True
    )

    class Meta:
        verbose_name = u'Вариант'
        verbose_name_plural = u'Варианты'

    def __unicode__(self):
        return self.name


class LineOptionChoice(models.Model):
    basket_line = models.ForeignKey(
        Line,
        related_name='options_choices',
        verbose_name=u'Строка корзины'
    )

    variant = models.ForeignKey(
        OptionInfo,
        verbose_name=u'Выбраный вариант',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        app_label = 'basket'
        verbose_name = u'Опция строки корзины'
        verbose_name_plural = u'Опции строки корзин'

    def __unicode__(self):
        return '%s'%(self.variant.variant.name)


class PackageOptionChoice(models.Model):
    package = models.ForeignKey(
        'ProductPackage',
        related_name='options_choices',
        verbose_name=u'Упаковка'
    )

    variant = models.ForeignKey(
        'OptionInfo',
        verbose_name=u'Выбраный вариант',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = u'Опция упаковки'
        verbose_name_plural = u'Опции упаковок'

    def __unicode__(self):
        return '%s' % (self.variant.variant.name)


class ProductPackage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name=u'packages',
        verbose_name=u'Товар'
    )

    package_num = models.IntegerField(
        verbose_name=u'Номер упаковки',
        default=1
    )

    count = models.IntegerField(
        verbose_name=u'Количество упаковок',
        default=1
    )

    upc = models.CharField(
        verbose_name=u'Артикул',
        max_length=20
    )

    name = models.CharField(
        verbose_name=u'Наименование упаковки',
        max_length=100
    )

    def render_name(self, **kwargs):
        temp = Template(self.name)
        return temp.render(Context(kwargs))

    class Meta:
        verbose_name = u'Упаковка'
        verbose_name_plural = u'Упаковки'

    def __unicode__(self):
        return u'Уп.%d %s'%(self.package_num, self.name)


class XMLDownloader(models.Model):
    msg = u'Загрузите правильный XML файл. ' + \
           u'Файл, который Вы загрузили, поврежден или не является XML файлом'
    description = models.CharField(
        max_length=128,
        verbose_name=u'Краткое описание',
    )
    xml = models.FileField(
        verbose_name=u'XML файл',
        help_text=u'XML',
    )
    creation_date = models.DateField(
        verbose_name=u'Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = u'XML файл'
        verbose_name_plural = u'XML файлы'

    def __unicode__(self):
        return self.description

    def file(self):
        return '<a href="/{}" target="_blank" class="button">Просмотреть файл</a>'.format(self.xml)

    def clean(self, *args, **kwargs):
        try:
            if self.xml:
                etree.parse(self.xml)
        except etree.XMLSyntaxError as e:
            raise ValidationError(self.msg)

    def save(self, *args, **kwargs):
        files = os.listdir(settings.MEDIA_ROOT)
        if str(self.xml) in files:
            try:
                storage = self.xml.storage
                path = self.xml.path
                storage.delete(path)
                try:
                    XMLDownloader.objects.filter(xml="./" + str(self.xml)).delete()
                except:
                    raise ValidationError(self.msg)
            except:
                raise ValidationError(self.msg)
        super(XMLDownloader, self).save(*args, **kwargs)

    def remove(self):
        file = self.id
        return '<a href="{}/delete/" class="deletelink">Удалить</a>'.format(file)

    def delete(self):
        try:
            XMLDownloader.objects.filter(id=self.id).delete()
        except:
            raise ValidationError(self.msg)
        try:
            storage = self.xml.storage
            path = self.xml.path
            storage.delete(path)
        except:
            raise ValidationError(self.msg)

    remove.allow_tags = True
    file.allow_tags = True


class Services(models.Model):
    free_delivery_from = models.DecimalField(verbose_name=u'Бесплатная доставка от, грн.',
                                             max_digits=7,
                                             decimal_places=2
                                             )
    lifting = models.DecimalField(u'Занос в квартиру от, грн.',
                                  max_digits=7,
                                  decimal_places=2
                                  )
    installation = models.DecimalField(u'Сборка, % от стоимости',
                                       max_digits=5,
                                       decimal_places=2
                                       )
    is_relevant = models.BooleanField(u'Актуальная информация')

    class Meta:
        verbose_name = u'Информация об услугах'
        verbose_name_plural = u'Информация об услугах'


from oscar.apps.catalogue.models import *
