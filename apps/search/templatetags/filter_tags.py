from django import template

from apps.search.forms import FilterForm

register = template.Library()


@register.inclusion_tag('partials/filters.html')
def draw_filter_form():
    return {'form':FilterForm()}