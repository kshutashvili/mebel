from oscar.apps.catalogue.admin import *

from oscar.apps.catalogue.admin import AttributeInline, CategoryInline, ProductRecommendationInline,\
    ProductAdmin as CoreProductAdmin

from django.contrib import admin
from django import forms

from .models import LineOptionChoice, MultipleOption, OptionGroup, OptionVariant



class MultipleOptionAdminInline(admin.TabularInline):
    model = MultipleOption
    extra = 2
    filter_horizontal = ('choices',)

class OptionVariantAdminInline(admin.TabularInline):
    model = OptionVariant
    extra = 3


class ProductAdmin(CoreProductAdmin):
    inlines = [AttributeInline, CategoryInline, MultipleOptionAdminInline, ProductRecommendationInline]



class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [OptionVariantAdminInline]

admin.site.register(LineOptionChoice)
admin.site.register(MultipleOption)
admin.site.register(OptionVariant)
admin.site.unregister(Product)

admin.site.register(OptionGroup, OptionGroupAdmin)
admin.site.register(Product, ProductAdmin)
