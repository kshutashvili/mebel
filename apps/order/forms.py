#-*-coding:utf8-*-

from django import forms
from .models import SimpleOrder, OneClickOrder


class SimpleOrderForm(forms.ModelForm):
    phone = forms.RegexField(widget=forms.TextInput(attrs={'placeholder': u'Ваш телефон'}),
                                            regex=r'^\+?1?\d{9,15}$',
                                            error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))

    class Meta:

        model = SimpleOrder
        exclude = ('basket','check_blank', 'order_status')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':u'Ваше имя'}),
            'comment': forms.Textarea(attrs={'placeholder': u'Коментарий'}),
            'email': forms.TextInput(attrs={'placeholder': u'E-mail'}),
            'region': forms.TextInput(attrs={'placeholder': u'Регион'}),
            'address': forms.TextInput(attrs={'placeholder': u'Адрес'}),
        }


class OneClickOrderForm(forms.ModelForm):
    phone = forms.RegexField(widget=forms.TextInput(attrs={'placeholder': u'(0XX)XXX - XX - XX'}),
                             regex=r'^\+?1?\d{9,15}$',
                             error_message=(
                             "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
                             label=''
                             )

    class Meta:
        model = OneClickOrder
        fields = ['phone']