# -*-coding:utf8-*-

from oscar.apps.search.forms import *
from oscar.apps.search.forms import SearchForm as CoreSearchForm

from django import forms

from apps.catalogue.models import OptionGroup


class FilterOptionField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '%s %s'%(obj.name, obj.group.postfix)


class FilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        self.make_filter()

    def make_filter(self):
        for group in OptionGroup.objects.all():
            self.fields['filter_%s'%group.code] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                        label=group.name,
                                                        choices=[(i.id, '%s %s'%(i.name, group.postfix))for i in group.variants.all()],
                                                        required=False
                                                        )


class SearchForm(CoreSearchForm, FilterForm):
    def search(self):
        sqs = super(SearchForm, self).search()
        return sqs
