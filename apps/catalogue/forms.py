from ckeditor.widgets import CKEditorWidget
from django import forms
from treebeard.forms import movenodeform_factory

from .models import Product, Category


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = CKEditorWidget()

    class Meta:
        model = Product
        fields = '__all__'


class CategoryForm(movenodeform_factory(Category)):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = CKEditorWidget()

