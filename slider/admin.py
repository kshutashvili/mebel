from django.contrib import admin

from .models import SliderSlide
# Register your models here.


@admin.register(SliderSlide)
class SliderSlideAdmin(admin.ModelAdmin):
    list_display = ('image', 'link')