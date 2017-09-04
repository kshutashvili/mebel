from django.contrib import admin

from .models import Catalog, Popular


class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin_photo', 'pdf', 'creation_date', 'description', )

class PopularAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin_photo', 'pdf', 'creation_date', 'description', )


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Popular, PopularAdmin)
