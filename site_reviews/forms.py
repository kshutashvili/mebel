# -*-coding:utf8-*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_model

from .models import SiteReview


class SiteReviewForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':u'Ваше имя'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':u'Ваш e-mail'}), required=True)

    def __init__(self, user=None, *args, **kwargs):
        print(kwargs)
        super(SiteReviewForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated():
            self.instance.user = user
            del self.fields['name']
            del self.fields['email']

    class Meta:
        model = SiteReview
        fields = ('score', 'body', 'name', 'email')
        widgets={
            'body':forms.Textarea(attrs={'placeholder':u'Ваше сообщение...', 'cols':'30', 'rows':'10'})
        }
        labels={
            'score': u'Оцените качество магазина',
            'body': '',
            'name': '',
            'email': ''
        }