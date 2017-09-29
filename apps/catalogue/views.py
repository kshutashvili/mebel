# coding: utf-8

from oscar.apps.catalogue.views import *
from oscar.apps.catalogue.views import CatalogueView as CoreCatalogueView, \
    ProductCategoryView as CoreProductCategoryView, \
    ProductDetailView as CoreProductDetailView

from oscar.core.loading import get_class, get_model

from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from filter.forms import FilterForm

from apps.basket.forms import AddToBasketForm
from apps.order.forms import OneClickOrderForm
from apps.catalogue.reviews.forms import ProductReviewForm
from common.views import AjaxFormMixin
from .models import XMLDownloader


get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')


class ProductDetailView(CoreProductDetailView):

    def get_context_data(self, **kwargs):
        ctx = super(ProductDetailView, self).get_context_data()

        self.form = AddToBasketForm(self.request.basket, self.object, self.request.GET)
        self.form.is_valid()
        ctx['price'] = self.form.options_product_price(self.request)
        ctx['review_form'] = ProductReviewForm(self.object)
        ctx['oneclick_form'] = OneClickOrderForm()
        return ctx


class CatalogueView(CoreCatalogueView):

    def get(self, request, *args, **kwargs):

        self.form = FilterForm(request.GET)
        options = []
        if self.form.is_valid():
            options = self.form.cleaned_data
        try:
            self.search_handler = self.get_search_handler(
                self.request.GET, request.get_full_path(), [], options)
        except InvalidPage:
            # Redirect to page one.
            messages.error(request, _('The given page number was invalid.'))
            return redirect('catalogue:index')
        return super(CoreCatalogueView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(CatalogueView, self).get_context_data(**kwargs)
        ctx['filter_form'] = self.form

        return ctx


class ProductCategoryView(CoreProductCategoryView):

    def get(self, request, *args, **kwargs):
        # Fetch the category; return 404 or redirect as needed

        self.category = self.get_category()
        potential_redirect = self.redirect_if_necessary(
            request.path, self.category)
        if potential_redirect is not None:
            return potential_redirect


        self.form=FilterForm(request.GET)
        options = []
        if self.form.is_valid():
            options = self.form.cleaned_data

        try:
            self.search_handler = self.get_search_handler(
                request.GET, request.get_full_path(), self.get_categories(), options)

        except InvalidPage:
            messages.error(request, _('The given page number was invalid.'))
            return redirect(self.category.get_absolute_url())


        print
        return super(CoreProductCategoryView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        ctx = super(ProductCategoryView, self).get_context_data(**kwargs)
        ctx['canonical'] = (self.search_handler.kwargs['page'] != 1)
        ctx['filter_form'] = self.form
        return ctx


class OneClickOrderCreateView(AjaxFormMixin, CreateView):
    form_class = OneClickOrderForm
    product_model = Product

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(
            self.product_model, pk=kwargs['pk'])
        return super(OneClickOrderCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.product = self.product
        instance.save()

        message = get_template('email/oneclick_order.html').render({'instance': instance})
        subject = u'Заявка на заказ(в один клик) №%s' % instance.id
        msg = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL, ])
        msg.attach_alternative(message, "text/html")
        msg.send()
        return HttpResponse(self.product.get_absolute_url())


def XMLDownloaderView(request):
    path = 'media' + request.path
    xml = open(path).read()
    response = HttpResponse(content_type='text/xml')
    response.write(xml)
    return response


def AddProductToFavorite(request, product_slug, pk):
    product = get_object_or_404(Product, pk=pk)
    request.favlist.add(product)
    url = request.GET.get('next') or '/favlist/'
    return redirect(url)


def RemoveProductFromFavorite(request, product_slug, pk):
    product = get_object_or_404(Product, pk=pk)
    request.favlist.remove(product)
    url = request.GET.get('next') or '/favlist/'
    return redirect(url)