#-*-coding:utf8-*-

from oscar.apps.basket.forms import *
from oscar.apps.basket.forms import AddToBasketForm as CoreAddToBasketForm

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


class ImageChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return mark_safe("<img src='%s'/>" % obj.image.url) if obj.image else obj.name


class AddToBasketForm(CoreAddToBasketForm):

    def __init__(self, basket, product, *args, **kwargs):
        super(AddToBasketForm, self).__init__(basket, product, *args, **kwargs)
        self._create_option_fields()

    def _create_option_fields(self):
        for option in self.parent_product.multiple_options.all():
            choices = []
            if option.display_type == 'radio':
                widget = forms.RadioSelect()
            else:
                widget = forms.Select()

            self.fields[option.group.code] = ImageChoiceField(widget=widget, queryset=option.choices.all(), label=option.group.name, required=True, empty_label=None)

    def cleaned_multiple_options(self):
        options = []
        for option in self.parent_product.multiple_options.all():
            if option.group.code in self.cleaned_data:
                options.append({
                    'multi_option': option,
                    'value': self.cleaned_data[option.group.code]})

        return options


class SimpleAddToBasketForm(AddToBasketForm):
    quantity = forms.IntegerField(
        initial=1, min_value=1, widget=forms.HiddenInput, label=_('Quantity'))

