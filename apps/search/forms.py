# -*-coding:utf8-*-

from oscar.apps.search.forms import *
from oscar.apps.search.forms import SearchForm as CoreSearchForm

from django import forms

from apps.catalogue.models import OptionGroup


class SearchForm(CoreSearchForm):
    def search(self):
        sqs = super(SearchForm, self).search()
        return sqs
