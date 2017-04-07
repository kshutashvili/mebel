from oscar.apps.catalogue.admin import *
from oscar.apps.catalogue.admin import AttributeInline, CategoryInline, ProductRecommendationInline,\
    ProductAdmin as CoreProductAdmin, CategoryAdmin as CoreCategoryAdmin

from django.contrib import admin

from .models import LineOptionChoice, MultipleOption, \
    OptionGroup, OptionVariant, OptionInfo, ProductPackage
from .forms import ProductForm

import nested_admin


class OptionInfoAdminInline(nested_admin.NestedStackedInline):
    model = OptionInfo
    extra = 1
    fk_name = 'multi_option'


class MultipleOptionAdminInline(nested_admin.NestedStackedInline):
    model = MultipleOption
    extra = 0
    inlines = [OptionInfoAdminInline, ]
    fk_name = 'product'


class OptionVariantAdminInline(admin.TabularInline):
    model = OptionVariant
    extra = 3


class ProductPackageAdminInline(admin.TabularInline):
    model = ProductPackage
    extra = 1


class CategoryAdmin(CoreCategoryAdmin, nested_admin.NestedModelAdmin):
    pass

class ProductAdmin(CoreProductAdmin, nested_admin.NestedModelAdmin):
    inlines = [AttributeInline, CategoryInline, MultipleOptionAdminInline, ProductRecommendationInline, ProductPackageAdminInline]
    form = ProductForm


class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [OptionVariantAdminInline]

admin.site.register(LineOptionChoice)
admin.site.register(MultipleOption)
admin.site.register(OptionVariant)
admin.site.unregister(Category)
admin.site.register(Category, CategoryAdmin)

admin.site.unregister(Product)
admin.site.register(OptionInfo)

admin.site.register(OptionGroup, OptionGroupAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.unregister(Option)
admin.site.unregister(AttributeOptionGroup)
admin.site.unregister(ProductAttribute)