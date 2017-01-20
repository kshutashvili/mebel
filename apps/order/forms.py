#-*-coding:utf8-*-

from django import forms
from .models import SimpleOrder


class SimpleOrderForm(forms.ModelForm):

    class Meta:
        model = SimpleOrder
        exclude = ('basket',)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':u'Ваше ммя'}),
            'phone': forms.TextInput(attrs={'placeholder': u'Ваш телефон'}),
            'comment': forms.Textarea(attrs={'placeholder': u'Коментарий'}),
            'country': forms.TextInput(attrs={'placeholder': u'Страна'}),
            'region': forms.TextInput(attrs={'placeholder': u'Регион'}),
            'city': forms.TextInput(attrs={'placeholder': u'Город'}),
            'address': forms.TextInput(attrs={'placeholder': u'Адрес'}),
        }