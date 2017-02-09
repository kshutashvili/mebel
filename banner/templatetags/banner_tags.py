from django import template
from banner.models import Banner

register = template.Library()

@register.inclusion_tag('banner/banner_list.html')
def banners(postion):
    banners = Banner.objects.filter(display=True)
    if postion:
        banners = banners.filter(position=int(postion))

    return {'banners':banners}