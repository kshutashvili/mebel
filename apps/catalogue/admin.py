from oscar.apps.catalogue.admin import *

from oscar.apps.catalogue.admin import AttributeInline, CategoryInline, ProductRecommendationInline,\
    ProductAdmin as CoreProductAdmin

from django.contrib import admin

from .models import LineOptionChoice, MultipleOption, OptionGroup, OptionVariant, OptionInfo
from .forms import OptionInfoForm

from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class OptionInfoAdminInline(NestedStackedInline):
    model = OptionInfo
    extra = 1
    form = OptionInfoForm
    fk_name = 'multi_option'


class MultipleOptionAdminInline(NestedStackedInline):
    model = MultipleOption
    extra = 0
    inlines = [OptionInfoAdminInline, ]
    fk_name = 'product'


class OptionVariantAdminInline(admin.TabularInline):
    model = OptionVariant
    extra = 3


class ProductAdmin(CoreProductAdmin, NestedModelAdmin):
    inlines = [AttributeInline, CategoryInline, MultipleOptionAdminInline, ProductRecommendationInline]


class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [OptionVariantAdminInline]

admin.site.register(LineOptionChoice)
admin.site.register(MultipleOption)
admin.site.register(OptionVariant)
admin.site.unregister(Product)

admin.site.register(OptionGroup, OptionGroupAdmin)
admin.site.register(Product, ProductAdmin)
