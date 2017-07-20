# -*-coding:utf8-*-

from oscar.apps.basket.forms import *
from oscar.apps.basket.forms import AddToBasketForm as CoreAddToBasketForm

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode


class ImageChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return mark_safe("<img src='%s'/>" % obj.variant.image.url) \
            if obj.variant.image \
            else mark_safe('%s %s' % (obj.variant.name, obj.variant.group.postfix))


class ImageMultipleChoiceField(forms.ModelMultipleChoiceField, ImageChoiceField):
    pass


class AddToBasketForm(CoreAddToBasketForm):
    def __init__(self, basket, product, *args, **kwargs):
        super(AddToBasketForm, self).__init__(basket, product, *args, **kwargs)
        self._create_option_fields()

    def _create_option_fields(self):
        radio_num = 0
        select_num = 0
        checkbox_num = 0
        for option in self.parent_product.multiple_options.all():
            choices = []
            params = {'queryset': option.choices.all(),
                      'label': option.group.name,
                      'required': option.is_required
                      }
            display_type = option.group.display_type

            if display_type == 'radio' or display_type == 'select':
                field = ImageChoiceField
                params['empty_label'] = None

                if display_type == 'radio':
                    params['widget'] = forms.RadioSelect(attrs={'class': 'option'})
                    radio_num += 1
                elif display_type == 'select':
                    params['widget'] = forms.Select(attrs={'class': 'option'})
                    params['empty_label'] = None
                    select_num += 1
            else:
                params['widget'] = forms.CheckboxSelectMultiple(attrs={'class': 'option'})
                field = ImageMultipleChoiceField
                checkbox_num += 1

            self.fields[option.group.code] = field(**params)
        self.radio_num = radio_num
        self.select_num = select_num
        self.checkbox_num = checkbox_num

    def cleaned_multiple_options(self):
        options = []
        data = self.cleaned_data
        for option in self.parent_product.multiple_options.all():
            if option.group.code in data and data[option.group.code]:
                if hasattr(data[option.group.code], '__iter__'):
                    for nested_option in data[option.group.code]:
                        options.append({
                            'multi_option': option,
                            'value': nested_option})
                else:
                    options.append({
                        'multi_option': option,
                        'value': data[option.group.code]})

        return options

    def options_product_price(self, request):
        data = self.cleaned_multiple_options()
        additional = 0
        for option in data:
            if option['value']:
                try:
                    add_price = option['value'].additional_price
                except AttributeError:
                    add_price = sum([nested_option.additional_price
                                     for nested_option in option['value']
                                     if nested_option.additional_price]
                                    )
                finally:
                    if add_price:
                        additional += add_price

        if self.product.is_parent:
            session = request.strategy.fetch_for_parent(self.product)
        else:
            session = request.strategy.fetch_for_product(self.product)

        base_price = session.price.incl_tax if session.price.incl_tax else session.price.excl_tax
        if base_price:
            return base_price + additional
        else:
            return 0


class SimpleAddToBasketForm(AddToBasketForm):
    quantity = forms.IntegerField(
        initial=1, min_value=1, widget=forms.HiddenInput, label=_('Quantity'))
