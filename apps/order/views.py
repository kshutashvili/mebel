# -*-coding:utf-8-*-

from django.views.generic import CreateView, FormView
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest

import json

from .forms import SimpleOrderForm

from django.shortcuts import redirect


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
        self.request.basket.submit()
        return HttpResponse(self.success_url)


