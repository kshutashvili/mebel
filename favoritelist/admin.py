from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.FavoriteList)
admin.site.register(models.FavoriteListLine)
