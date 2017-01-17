from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_model

from .models import SiteReview


class SiteReviewForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), required=True)
    email = forms.EmailField(label=_('Email'), required=True)

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