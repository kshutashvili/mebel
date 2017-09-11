from django.contrib import admin

from .models import Catalog, Popular


class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin_photo', 'description', 'creation_date', 'pdf', )
    list_display_links = ('id', 'admin_photo', 'description', )


class PopularAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin_photo', 'description', 'creation_date', 'pdf', )
    list_display_links = ('id', 'admin_photo', 'description', )


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Popular, PopularAdmin)
