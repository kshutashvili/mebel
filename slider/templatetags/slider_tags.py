from django import template

from slider.models import SliderSlide

register = template.Library()


@register.inclusion_tag('slider/slider.html')
def draw_slider():
    return {'slides': SliderSlide.objects.all()}