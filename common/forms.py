# -*-coding: utf8-*-
from django import forms

from common.models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ContactMessageForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Ваше имя'}
        self.fields['email'].widget.attrs = {'placeholder': 'Ваш e-mail'}
        self.fields['message'].widget.attrs = {'placeholder': 'Ваш вопрос...'}
        if request:
            self.fields['name'].initial = request.user.first_name
            self.fields['email'].initial = request.user.email
