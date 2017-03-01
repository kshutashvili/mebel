from django import forms

from apps.catalogue.models import OptionGroup


class FilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        self.make_filter()

    def make_filter(self):
        for group in OptionGroup.objects.filter(is_filter=True):
            self.fields[u'filter_%s'%group.code] = \
                forms.MultipleChoiceField(
                    widget=forms.CheckboxSelectMultiple(),
                    label=group.name,
                    choices=[(i.id, u'%s %s'%(i.name, group.postfix))for i in group.variants.all()],
                    required=False
                )