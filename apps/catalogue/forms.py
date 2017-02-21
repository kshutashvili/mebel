from .models import Product

from django import forms

from ckeditor.widgets import CKEditorWidget


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = CKEditorWidget()

    class Meta:
        model = Product
        fields = '__all__'