from django import forms

from .models import OptionInfo, MultipleOption, OptionVariant


class OptionInfoForm(forms.ModelForm):
    class Meta:
        model = OptionInfo
        fields = '__all__'
