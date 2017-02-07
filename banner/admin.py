from django.contrib import admin

from . import models

# Register your models here.


class BannerAdmin(admin.ModelAdmin):
    model = models.Banner
    list_display = ('link', 'when_created', 'display', 'position')
    list_filter = ('position', 'display')


admin.site.register(models.Banner, BannerAdmin)