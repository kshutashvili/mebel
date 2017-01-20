from oscar.apps.order.admin import *  # noqa

from .models import SimpleOrder

admin.site.register(SimpleOrder)