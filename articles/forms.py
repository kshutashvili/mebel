from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = CKEditorWidget()


    class Meta:
        model = Article
        fields = '__all__'