from oscar.apps.order.admin import *  # noqa

from .models import SimpleOrder, ShippingCity

admin.site.register(SimpleOrder)
admin.site.register(ShippingCity)

admin.site.unregister(Order)
admin.site.unregister(Line)
admin.site.unregister(LinePrice)
admin.site.unregister(LineAttribute)
admin.site.unregister(OrderNote)
admin.site.unregister(PaymentEvent)
admin.site.unregister(PaymentEventType)
admin.site.unregister(CommunicationEvent)
admin.site.unregister(ShippingEvent)
admin.site.unregister(ShippingEventType)
admin.site.unregister(OrderDiscount)

