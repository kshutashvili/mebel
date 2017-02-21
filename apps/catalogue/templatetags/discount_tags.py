from django import template

register = template.Library()

@register.filter()
def cut_percent(val):
    a = str(val)
    return a[:len(a)-3]
