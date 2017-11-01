from ckeditor.widgets import CKEditorWidget
from django import forms
from treebeard.forms import movenodeform_factory

from .models import Product, Category, PackageOptionChoice, OptionInfo


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

#
# class PackageOptionChoiceForm(forms.ModelForm):
#     class Meta:
#         model = PackageOptionChoice
#
#     def __init__(self, *args, **kwargs):
#         super(PackageOptionChoiceForm, self).__init__(*args, **kwargs)
#         self.fields['variant'].choices = OptionInfo.objects.filter(multi_option__product=)