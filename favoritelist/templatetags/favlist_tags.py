from django import template

register = template.Library()

@register.filter
def favlist_exist(val, wishlist):
    return wishlist.exist(val)