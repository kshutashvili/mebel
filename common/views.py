# -*-coding: utf8-*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import CreateView, FormView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseBadRequest

from common.models import ContactMessage
from common.forms import ContactMessageForm


class AjaxFormMixin(FormView):
    def form_valid(self, form):
        return HttpResponse(self.success_url)

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors.as_json())


class ContactsView(TemplateView):
    template_name = 'common/contacts.html'

    def get_context_data(self, **kwargs):
        context = super(ContactsView, self).get_context_data(**kwargs)
        context['form'] = ContactMessageForm(request=self.request)
        return context


class MessageView(CreateView):
    model = ContactMessage
    form_class = ContactMessageForm
    success_url = reverse_lazy('common:contacts')
    http_method_names = ['post']

    def form_valid(self, form):
        message = _('Спасибо за сообщение.')
        messages.success(self.request, message)
        return super(MessageView, self).form_valid(form)
