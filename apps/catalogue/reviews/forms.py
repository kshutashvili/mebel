# -*-coding:utf8-*-

from oscar.apps.catalogue.reviews.forms import *
from oscar.apps.catalogue.reviews.forms import ProductReviewForm as CoreProductReviewForm
from .models import ProductReview


class ProductReviewForm(CoreProductReviewForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Ваше имя'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': u'Ваш e-mail'}), required=True)

    class Meta:
        model = ProductReview
        fields = ('score', 'body', 'name', 'email')
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': u'Ваше сообщение...', 'cols': '30', 'rows': '10'})
        }
        labels = {
            'score': u'Оцените качество магазина',
            'body': '',
            'name': '',
            'email': ''
        }