# -*-coding:utf-8-*-

from django.views.generic import CreateView, FormView
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import get_template
from django.conf import settings

from .forms import SimpleOrderForm

from django.core.mail import EmailMultiAlternatives


class AjaxFormMixin(FormView):
    def form_valid(self, form):
        return HttpResponse('OK')

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors.as_json())


class SimpleOrderView(AjaxFormMixin, CreateView):
    form_class = SimpleOrderForm
    template_name = 'checkout/order.html'
    context_object_name = 'order_form'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.basket = self.request.basket
        instance.save()
        self.send_mail(instance)
        self.request.basket.submit()
        return HttpResponse(self.success_url)

    def send_mail(self, order):
        message = get_template('email/tanks_order.html').render({'order':order})
        subject = u'Заказ №%s' % order.id
        msg = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [order.email, ])
        msg.attach_alternative(message, "text/html")

        msg.attach_file(order.check_blank.path)
        msg.attach_file(order.manufacture_blank.path)
        msg.attach_file(order.shipping_blank.path)
        msg.send()