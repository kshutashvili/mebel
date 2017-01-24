# -*-coding:utf8-*-

from oscar.apps.catalogue.abstract_models import AbstractProduct

from apps.basket.models import Line

from django.db import models
from django.core.exceptions import ValidationError


class Product(AbstractProduct):
    def get_preview_info(self):
        prev_list = []
        for moption in self.multiple_options.all():
            if moption.group.preview:
                prev_list.append('%s(%s)' % (moption.choices.all()[0].name,
                                             ','.join([var.name for var in moption.choices.all()[1:]])))

        return 'X'.join(prev_list)


class MultipleOption(models.Model):
    product = models.ForeignKey('Product', related_name='multiple_options', verbose_name=u'Товар')
    group = models.ForeignKey('OptionGroup', related_name='Choices', verbose_name=u'Група опций', default=1)
    choices = models.ManyToManyField('OptionVariant', verbose_name=u'Варианты')

    class Meta:
        verbose_name = u'Множественная опция'
        verbose_name_plural = u'Множественные опции'

    def __unicode__(self):
        return self.group.code


class OptionGroup(models.Model):
    TYPE_CHOICES = (
        ('radio', 'radio'),
        ('select', 'select')
    )

    name = models.CharField(max_length=100, verbose_name=u'Название групы')
    code = models.CharField(max_length=100, verbose_name=u'Код групы', help_text=u'Только латинские символы')
    display_type = models.CharField(choices=TYPE_CHOICES, default='radio', max_length=100, verbose_name=u'Тип отображения')
    preview = models.BooleanField(default=False)
    postfix = models.CharField(max_length=5, blank=True, default='', verbose_name=u'Постфикс')

    class Meta:
        verbose_name = u'Група опций'
        verbose_name_plural = u'Групы опций'

    def __unicode__(self):
        return self.name


class OptionVariant(models.Model):
    group = models.ForeignKey(OptionGroup, related_name='variants', verbose_name=u'Група')
    name = models.CharField(max_length=100,verbose_name=u'Название')
    image = models.ImageField(verbose_name=u'Изображение', upload_to='options_image', blank=True)

    class Meta:
        verbose_name = u'Вариант'
        verbose_name_plural = u'Варианты'

    def __unicode__(self):
        return self.name


class LineOptionChoice(models.Model):
    basket_line = models.ForeignKey(Line, related_name='options_choices', verbose_name=u'Строка корзины')
    option = models.ForeignKey(MultipleOption, verbose_name=u'Доступные варианты')
    variant = models.ForeignKey(OptionVariant, verbose_name=u'Выбраный вариант')

    class Meta:
        app_label = 'basket'
        verbose_name = u'Опция строки корзины'
        verbose_name_plural = u'Опции строки корзин'

    def __unicode__(self):
        return '%s %s: %s'%(self.basket_line, self.option.group.name, self.variant.name)


from oscar.apps.catalogue.models import *