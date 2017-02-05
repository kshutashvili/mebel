from oscar.apps.order.admin import *  # noqa

from .models import SimpleOrder, ShippingCity

admin.site.register(SimpleOrder)
admin.site.register(ShippingCity)